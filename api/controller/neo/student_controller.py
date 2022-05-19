from py2neo import Node, Relationship
import json
from db.neo4jdb.user import UserCreateSchema, UserUpdateSchema
from db.neo4jdb.neo import graph

# TODO: return
def get_all_students():
    result = graph.nodes.match("Student").all()
    return json.dumps([{"student": dict(row["student"])} for row in result])


# TODO: return
def get_by_name(name):
    result = graph.nodes.match("Student", name=name)
    return json.dumps([{"student": dict(row["student"])} for row in result])


# TODO: return
def delete_by_name(name):
    result = graph.run(
        "MATCH (s:Student) {name: $name} "
        "DETACH DELETE s"
    )


# TODO: return
def edit_student(name, editStudent: UserUpdateSchema):
    email = editStudent.email
    born = editStudent.born
    password_hash = editStudent.password_hash
    result = graph.run(
        "MATCH (s:Student) {name: $name} "
        "SET s.email: $email, s.born: $born, s.password_hash: $password_hash"
    )


# TODO: functionality
def create_student(createStudentObject: UserCreateSchema):
    studentNode = Node("Student", name=createStudentObject.name, email=createStudentObject.email,
                       born=createStudentObject.born, password_hash= createStudentObject.password_hash)
    tx = graph.begin()
    tx.create(studentNode)
    if (createStudentObject.courseName != None):
        studentRelship = Relationship(studentNode, "IS_ENROLLED_IN_COURSE", createStudentObject.courseName)
        tx.create(studentRelship)
    tx.commit()
