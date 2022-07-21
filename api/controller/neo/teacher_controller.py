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

def get_all_teachers():
    result = graph.nodes.match("Teacher").all()
    return result

def get_by_name(name):
    result = graph.nodes.match("Teacher", name=name).first()
    return result

def get_by_email(email):
    result = graph.nodes.match("Teacher", email=email).first()
    return result

# TODO return
def get_password_hash_by_email(email):
    result = graph.run(f'MATCH (t:Teacher {{email: "{email}"}}) return t.password_hash').data()
    return result

def get_by_course_name(name):
    query = f'MATCH (c:Course {{name: "{name}"}})-[:TAUGHT_BY]->(teacher) return teacher.name'
    result = graph.run(query).data()
    return result

def get_courses_taught_by_teacher(name):
    query = f'MATCH (c:Course)-[:TAUGHT_BY]->(t:Teacher {{name: "{name}"}}) return c.name'
    result = graph.run(query).data()
    return result

def delete_by_name(name):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Teacher", name=name).first()
    tx.delete(nodeToDelete)
    result = tx.commit()
    if result is None:
        return True

def edit_teacher(name, teacher: UserUpdate):
    if teacher.born is not None:
        born = teacher.born
        result = graph.run(
            f'MATCH (t:Teacher {{name: "{name}"}}) SET t.born= {born}'
        )
        return result.stats()
    elif teacher.courseName is not None:
        graph.run(f'MATCH (t:Teacher {{name: "{name}"}}), (c:Course {{name: "{teacher.courseName}"}}) CREATE (c)-[r:TAUGHT_BY]->(t)')
    else:
        return http.client.responses[http.client.BAD_REQUEST]

def create_teacher(teacher: UserCreate):
    teacherNode = Node("Teacher", name=teacher.name, email=teacher.email,
                       born=teacher.born, password_hash= get_password_hash(teacher.password))
    tx = graph.begin()
    tx.create(teacherNode)
    if teacher.courseName is not None:
        courseNode = graph.nodes.match("Course", name=teacher.courseName).first()
        teacherRelship = Relationship(courseNode, "TAUGHT_BY", teacherNode)
        tx.create(teacherRelship)
    result = tx.commit()
    if result is None:
        return True
