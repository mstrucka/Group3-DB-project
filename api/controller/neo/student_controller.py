from bson import json_util
from py2neo import Node, Relationship, NodeMatcher
import json
from db.neo4jdb.user import UserCreateSchema, UserUpdateSchema
from db.neo4jdb.neo import graph


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


# TODO: return
def edit_student(name, editStudent: UserUpdateSchema):
    if editStudent.born is not None:
        born = editStudent.born
        result = graph.run(
            "MATCH (s:Student) {name: $name} "
            "SET s.born: $born"
        )



# TODO: relationship, hash PW
def create_student(createStudentObject: UserCreateSchema):
    studentNode = Node("Student", name=createStudentObject.name, email=createStudentObject.email,
                       born=createStudentObject.born, password_hash=createStudentObject.password)
    tx = graph.begin()
    tx.create(studentNode)
    if (createStudentObject.courseName != None):
        studentRelship = Relationship(studentNode, "IS_ENROLLED_IN_COURSE", createStudentObject.courseName)
        tx.create(studentRelship)
    tx.commit()
