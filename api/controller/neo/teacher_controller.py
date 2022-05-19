from py2neo import Graph, Node, Relationship
import os
import json

from db.neo4jdb.user import UserCreateSchema, UserUpdateSchema

# TODO: connection
# uri = os.getenv("NEO4J_URI")
# user = os.getenv("NEO4J_NAME")
# password = os.getenv("NEO4J_PASS")
# my_graph = Graph(uri, auth=(user, password))


# TODO: return
def get_all_teachers():
    result = Graph().nodes.match("Teacher").all()
    return json.dumps([{"teacher": dict(row["teacher"])} for row in result])


# TODO: return
def get_by_name(name):
    result = Graph().nodes.match("Teacher", name=name)
    return json.dumps([{"teacher": dict(row["teacher"])} for row in result])


# TODO: check functionality
def get_by_course_name(name):
    Graph().nodes.match(name=name).first()
    result = Graph().match(nodes=[name], r_type="TAUGHT_BY").all()
    return json.dumps({"teacher": result})


# TODO: return
def delete_by_name(name):
    Graph().delete("Teacher", name=name)


# TODO: return
def edit_teacher(name, editTeacher: UserUpdateSchema):
    email = editTeacher.email
    born = editTeacher.born
    password_hash = editTeacher.password_hash
    result = Graph().run(
        "MATCH (t:Teacher) {name: $name} "
        "SET t.email: $email, t.born: $born, t.password_hash: $password_hash"
    )


# TODO: check functionality
def create_teacher(createTeacherObject: UserCreateSchema):
    teacherNode = Node("Teacher", name=createTeacherObject.name,email=createTeacherObject.email,
                       born=createTeacherObject.born, password_hash= createTeacherObject.password_hash)
    tx = Graph().begin()
    tx.create(teacherNode)
    if (createTeacherObject.courseName != None):
        teacherRelship = Relationship(teacherNode, "TEACHES", createTeacherObject.courseName)
        tx.create(teacherRelship)
    tx.commit()
