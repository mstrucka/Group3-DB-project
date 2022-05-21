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
    result = graph.nodes.match("Teacher")
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        to_return.append(json_doc)
    return to_return


def get_by_name(name):
    result = graph.nodes.match("Teacher", name=name).first()
    return json.dumps(result, default=json_util.default)


def get_by_email(email):
    result = graph.nodes.match("Teacher", email=email).first()
    return json.dumps(result, default=json_util.default)


# TODO: still does not work
def get_by_course_name(name):
    graph.nodes.match(name=name).first()
    result = graph.match(nodes=[name], r_type="TAUGHT_BY").all()
    return json.dumps({"teacher": result})


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
    else:
        return http.client.responses[http.client.BAD_REQUEST]


def create_teacher(teacher: UserCreate):
    teacherNode = Node("Teacher", name=teacher.name, email=teacher.email,
                       born=teacher.born, password_hash= get_password_hash(teacher.password))
    tx = graph.begin()
    tx.create(teacherNode)
    if teacher.courseName is not None:
        courseNode = graph.nodes.match("Course", title=teacher.courseName).first()
        teacherRelship = Relationship(courseNode, "TAUGHT_BY", teacherNode)
        tx.create(teacherRelship)
    result = tx.commit()
    if result is None:
        return True
