from src.database.config import supabase
import bcrypt
import httpx

class DatabaseConnectionError(Exception):
    pass

def execute_query(query):
    try:
        return query.execute()
    except (
        httpx.RemoteProtocolError,
        httpx.ConnectError,
        httpx.ReadError,
        httpx.TimeoutException,
    ) as exc:
        raise DatabaseConnectionError(
            "Could not connect to the attendance database. Please check your internet connection and try again."
        ) from exc

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()

def check_pass(pwd,hashed):
    return bcrypt.checkpw(pwd.encode(),hashed.encode())




def check_teacher_exist(username):
    # check for unique username, returns false when username is already taken
    response=execute_query(supabase.table("teachers").select("username").eq("username",username))
    return len(response.data)>0


def create_teacher(username,password,name):

    data={"username":username,"password":hash_pass(password),"name":name}
    response=execute_query(supabase.table("teachers").insert(data))
    return response.data


def teacher_login(username,password):
    response=execute_query(supabase.table("teachers").select("*").eq("username",username))
    if response.data:
        teacher=response.data[0]
        if check_pass(password,teacher["password"]):
            return teacher
    return None

def get_all_students():
    response=execute_query(supabase.table("students").select("*"))
    return response.data

def create_student(new_name,face_embedding=None,voice_embedding=None):
    data={"name":new_name,"face_embedding":face_embedding,"voice_embedding":voice_embedding}
    response=execute_query(supabase.table("students").insert(data))
    return response.data

def update_student_biometrics(student_id,face_embedding=None,voice_embedding=None):
    data={}

    if face_embedding is not None:
        data["face_embedding"]=face_embedding

    if voice_embedding is not None:
        data["voice_embedding"]=voice_embedding

    if not data:
        return []

    response=execute_query(
        supabase
        .table("students")
        .update(data)
        .eq("student_id",student_id)
        .select("*")
    )
    return response.data


def create_subject(subject_code,name,section,teacher_id):
    data={"subject_code":subject_code,"name":name,"section":section,"teacher_id":teacher_id}
    response=execute_query(supabase.table("subjects").insert(data))
    return response.data

def get_teacher_subjects(teacher_id):
    response=execute_query(supabase.table("subjects").select("*,subject_students(count),attendence_logs(timestamp)").eq("teacher_id",teacher_id))
    subjects=response.data


    for sub in subjects:
        sub["total_student"] = (
        sub.get("subject_students", [{}])[0].get("count", 0)
        if sub.get("subject_students")
        else 0
        )
        attendance=sub.get("attendence_logs",[])
        unique_sessions=len(set(log["timestamp"] for log in attendance))
        sub["total_classes"]=unique_sessions

        sub.pop("subject_students",None)
        sub.pop("attendence_logs",None)

    return subjects

def enroll_student_to_subject(student_id,subject_id):
    data={'student_id':student_id,"subject_id":subject_id}
    response=execute_query(supabase.table('subject_students').insert(data))
    return response.data

def unenroll_student_to_subject(student_id,subject_id):
    response=execute_query(supabase.table('subject_students').delete().eq('student_id',student_id).eq('subject_id',subject_id))
    return response.data


def get_student_subjects(student_id):
    response=execute_query(supabase.table('subject_students').select('*,subjects(*)').eq('student_id',student_id))
    return response.data

def get_student_attendance(student_id):
    response=execute_query(supabase.table('attendence_logs').select('*').eq('student_id',student_id))
    return response.data


def create_attendance(logs):
    response=execute_query(supabase.table("attendence_logs").insert(logs))
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = execute_query(
        supabase
        .table("attendence_logs")   # corrected name
        .select("*,subjects!inner(*)")
        .eq("subjects.teacher_id", teacher_id)
    )
    return response.data
