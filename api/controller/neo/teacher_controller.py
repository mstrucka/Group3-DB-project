from pprint import pprint

from bson import json_util
from py2neo import Node, Relationship
import json
from db.neo4jdb.user import UserCreateSchema, UserUpdateSchema
from db.neo4jdb.neo import graph


# TODO: return
def get_all_teachers():
    result = graph.nodes.match("Teacher")
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        to_return.append(json_doc)
    return to_return


# TODO: return
def get_by_name(name):
    result = graph.nodes.match("Teacher", name=name)
    return json.dumps([{"teacher": dict(row["teacher"])} for row in result])


# TODO: return
def get_by_email(email):
    result = graph.nodes.match("Teacher", email=email)
    return result


# TODO: check functionality
def get_by_course_name(name):
    graph.nodes.match(name=name).first()
    result = graph.match(nodes=[name], r_type="TAUGHT_BY").all()
    return json.dumps({"teacher": result})


# TODO: return
def delete_by_name(name):
    graph.delete("Teacher", name=name)


# TODO: return
def edit_teacher(name, editTeacher: UserUpdateSchema):
    born = editTeacher.born
    result = graph.run(
        "MATCH (t:Teacher) {name: $name} "
        "SET t.born: $born"
    )


# TODO: check functionality, hash PW
def create_teacher(createTeacherObject: UserCreateSchema):
    teacherNode = Node("Teacher", name=createTeacherObject.name, email=createTeacherObject.email,
                       born=createTeacherObject.born, password_hash= createTeacherObject.password)
    tx = graph.begin()
    tx.create(teacherNode)
    if (createTeacherObject.courseName != None):
        teacherRelship = Relationship(teacherNode, "TEACHES", createTeacherObject.courseName)
        tx.create(teacherRelship)
    tx.commit()
