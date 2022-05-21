from pprint import pprint

from bson import json_util
from py2neo import Node, Relationship
import json
import http.client
from db.neo4jdb.user import UserCreateSchema, UserUpdateSchema
from db.neo4jdb.neo import graph


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


# TODO: check functionality
def get_by_course_name(name):
    graph.nodes.match(name=name).first()
    result = graph.match(nodes=[name], r_type="TAUGHT_BY").all()
    return json.dumps({"teacher": result})


# TODO: return
def delete_by_name(name):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Teacher", name=name).first()
    tx.delete(nodeToDelete)
    tx.commit()


# TODO: return check
def edit_teacher(tname, editTeacher: UserUpdateSchema):
    if editTeacher.born is not None:
        born = editTeacher.born
        result = graph.run(
            f'MATCH (t:Teacher {{name: "{tname}"}}) SET t.born= {born}'
        )
        return result.stats()
    else:
        return http.client.responses[http.client.BAD_REQUEST]


# TODO: relationship, hash PW
def create_teacher(createTeacherObject: UserCreateSchema):
    teacherNode = Node("Teacher", name=createTeacherObject.name, email=createTeacherObject.email,
                       born=createTeacherObject.born, password_hash= createTeacherObject.password)
    tx = graph.begin()
    tx.create(teacherNode)
    if (createTeacherObject.courseName != None):
        teacherRelship = Relationship(teacherNode, "TEACHES", createTeacherObject.courseName)
        tx.create(teacherRelship)
    tx.commit()
