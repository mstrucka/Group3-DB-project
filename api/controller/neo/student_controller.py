import http
from bson import json_util
from py2neo import Node, Relationship
import json
import http.client
from db.neo4jdb.user import UserCreate, UserUpdate
from db.neo4jdb.neo import graph
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)

def get_all_students():
    result = graph.nodes.match("Student").all()
    return result

def get_by_name(name):
    result = graph.nodes.match("Student", name=name).first()
    return result

def get_by_email(email):
    result = graph.nodes.match("Student", email=email).first()
    return result

#TODO
def get_password_hash_by_email(email):
    result = graph.run(f'MATCH (s:Student {{email: "{email}"}}) return s.password_hash').evaluate()
    return result

def get_enrollments_full(name):
    query= f'MATCH (s:Student {{name: "{name}"}})-[:IS_ENROLLED_IN_COURSE]->(course) return course'
    result = graph.run(query).data()
    return result

def get_enrollments_names(name):
    query= f'MATCH (s:Student {{name: "{name}"}})-[:IS_ENROLLED_IN_COURSE]->(course) return course.name'
    result = graph.run(query).data()
    return result


def delete_by_name(name):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Student", name=name).first()
    tx.delete(nodeToDelete)
    result = tx.commit()
    if result is None:
        return True


def delete_by_enrollment_by_course_name(studentName, courseName):
    result = graph.run(f'MATCH (s:Student {{name: "{studentName}"}})-[r:IS_ENROLLED_IN_COURSE]->(c: Course {{name: "{courseName}"}}) delete r')
    return result.stats()


def edit_student(name, student: UserUpdate):
    if student.born is not None:
        born = student.born
        result = graph.run(
            f'MATCH (s:Student {{name: "{name}"}}) SET s.born= {born}'
        )
        return result.stats()
    elif student.courseName is not None:
        graph.run(f'MATCH (s:Student {{name: "{name}"}}), (c:Course {{name: "{student.courseName}"}}) CREATE (s)-[r:IS_ENROLLED_IN_COURSE]->(c)')
    else:
        return http.client.responses[http.client.BAD_REQUEST]


def create_student(student: UserCreate):
    studentNode = Node("Student", name=student.name, email=student.email,
                       born=student.born, password_hash=student.password)
    tx = graph.begin()
    tx.create(studentNode)
    if student.courseName is not None:
        courseNode = graph.nodes.match("Course", name=student.courseName).first()
        studentRelship = Relationship(studentNode, "IS_ENROLLED_IN_COURSE", courseNode)
        tx.create(studentRelship)
    result = tx.commit()
    if result is None:
        return True
