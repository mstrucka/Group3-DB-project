from py2neo import Node, Relationship
import json
from db.neo4jdb.user import UserCreateSchema, UserUpdateSchema
from db.neo4jdb.neo import graph


# TODO: return
def get_all_students():
    result = graph.nodes.match("Student").all()
    print(result)
    return json.dumps([{"student": dict(row["student"])} for row in result])


# TODO: return
def get_by_name(name):
    result = graph.nodes.match("Student", name=name)
    return result


# TODO: return
def get_by_email(email):
    result = graph.nodes.match("Student", email=email)
    return result


# TODO: return
def delete_by_name(name):
    result = graph.delete("Student", name=name)


# TODO: return
def edit_student(name, editStudent: UserUpdateSchema):
    if editStudent.born is not None:
        born = editStudent.born
        result = graph.run(
            "MATCH (s:Student) {name: $name} "
            "SET s.born: $born"
        )



# TODO: functionality, hash PW
def create_student(createStudentObject: UserCreateSchema):
    studentNode = Node("Student", name=createStudentObject.name, email=createStudentObject.email,
                       born=createStudentObject.born, password_hash=createStudentObject.password)
    tx = graph.begin()
    tx.create(studentNode)
    if (createStudentObject.courseName != None):
        studentRelship = Relationship(studentNode, "IS_ENROLLED_IN_COURSE", createStudentObject.courseName)
        tx.create(studentRelship)
    tx.commit()
