from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


def get_voice_embedding(audio_bytes):
    """
    Generate a voice embedding from audio bytes.
    Returns the embedding as a list for database storage.
    """
    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True
        )

        audio = librosa.util.normalize(audio)

        wav = preprocess_wav(audio)

        embedding = encoder.embed_utterance(wav)

        return embedding.tolist()

    except Exception as e:
        st.error(f"Voice recognition error: {e}")
        return None


def identify_speaker(new_embedding, candidates_dict, threshold=0.65):

    if new_embedding is None:
        st.warning("New embedding is None")
        return None, 0.0

    if not candidates_dict:
        st.warning("No stored embeddings found")
        return None, 0.0

    new_embedding = np.asarray(new_embedding)

    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():

        if stored_embedding is None:
            continue

        stored_embedding = np.asarray(stored_embedding)

        if len(stored_embedding) != len(new_embedding):
            st.warning(
                f"Embedding size mismatch for {sid}: "
                f"{len(stored_embedding)} vs {len(new_embedding)}"
            )
            continue

        denominator = (
            np.linalg.norm(new_embedding)
            * np.linalg.norm(stored_embedding)
        )

        if denominator == 0:
            continue

        similarity = (
            np.dot(new_embedding, stored_embedding)
            / denominator
        )

        st.write(f"{sid}: {similarity:.4f}")

        if similarity > best_score:
            best_score = similarity
            best_sid = sid

    st.write(
        f"Best Match: {best_sid}, "
        f"Score: {best_score:.4f}"
    )

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


def process_bulk_audio(
    audio_bytes,
    candidates_dict,
    threshold=0.65
):
    """
    Identify multiple speakers from a long audio recording.

    Returns:
        {
            student_id: highest_similarity_score
        }
    """

    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True
        )

        audio = librosa.util.normalize(audio)

        segments = librosa.effects.split(
            audio,
            top_db=20
        )

        identified_results = {}

        for start, end in segments:

            duration = (end - start) / sr

            # Ignore segments shorter than 2 seconds
            if duration < 2:
                continue

            segment_audio = audio[start:end]

            wav = preprocess_wav(segment_audio)

            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(
                embedding,
                candidates_dict,
                threshold
            )

            if sid is not None:

                if (
                    sid not in identified_results
                    or score > identified_results[sid]
                ):
                    identified_results[sid] = score

        return identified_results

    except Exception as e:
        st.error(f"Bulk processing error: {e}")
        return {}