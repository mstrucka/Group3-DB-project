import http

from bson import json_util
from py2neo import Node, Relationship
import json
import http.client
from db.neo4jdb.user import UserCreateSchema, UserUpdateSchema
from db.neo4jdb.neo import graph
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)


def get_all_students():
    result = graph.nodes.match("Student")
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        to_return.append(json_doc)
    return to_return


def get_by_name(name):
    result = graph.nodes.match("Student", name=name).first()
    return json.dumps(result, default=json_util.default)


def get_by_email(email):
    result = graph.nodes.match("Student", email=email).first()
    return json.dumps(result, default=json_util.default)


# TODO: return
def delete_by_name(name):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Student", name=name).first()
    tx.delete(nodeToDelete)
    tx.commit()


# TODO: return check
def edit_student(sname, editStudent: UserUpdateSchema):
    if editStudent.born is not None:
        born = editStudent.born
        result = graph.run(
            f'MATCH (s:Student {{name: "{sname}"}}) SET s.born= {born}'
        )
        return result.stats()
    else:
        return http.client.responses[http.client.BAD_REQUEST]


# TODO: relationship, hash PW
def create_student(createStudentObject: UserCreateSchema):
    studentNode = Node("Student", name=createStudentObject.name, email=createStudentObject.email,
                       born=createStudentObject.born, password_hash=get_password_hash(createStudentObject.password))
    tx = graph.begin()
    tx.create(studentNode)
    if (createStudentObject.courseName != None):
        studentRelship = Relationship(studentNode, "IS_ENROLLED_IN_COURSE", createStudentObject.courseName)
        tx.create(studentRelship)
    tx.commit()
