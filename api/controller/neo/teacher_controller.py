from pprint import pprint
from py2neo import Node, Relationship
import json
from db.neo4jdb.user import UserCreateSchema, UserUpdateSchema
from db.neo4jdb.neo import graph


# TODO: return
def get_all_teachers():
    result = graph.nodes.match("Teacher").all()
    return result
    return json.dumps([{"teacher": dict(row["teacher"])} for row in result])


# TODO: return
def get_by_name(name):
    result = graph.nodes.match("Teacher", name=name)
    return json.dumps([{"teacher": dict(row["teacher"])} for row in result])


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
    email = editTeacher.email
    born = editTeacher.born
    password_hash = editTeacher.password_hash
    result = graph.run(
        "MATCH (t:Teacher) {name: $name} "
        "SET t.email: $email, t.born: $born, t.password_hash: $password_hash"
    )


# TODO: check functionality
def create_teacher(createTeacherObject: UserCreateSchema):
    teacherNode = Node("Teacher", name=createTeacherObject.name,email=createTeacherObject.email,
                       born=createTeacherObject.born, password_hash= createTeacherObject.password_hash)
    tx = graph.begin()
    tx.create(teacherNode)
    if (createTeacherObject.courseName != None):
        teacherRelship = Relationship(teacherNode, "TEACHES", createTeacherObject.courseName)
        tx.create(teacherRelship)
    tx.commit()
