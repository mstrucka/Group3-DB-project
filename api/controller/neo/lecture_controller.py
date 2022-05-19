from py2neo import Graph, Node, Relationship
import os
import json
from db.neo4jdb.neo import App

from db.neo4jdb.lecture import LectureCreateSchema, LectureUpdateSchema

# TODO: connection
# uri = os.getenv("NEO4J_URI")
# user = os.getenv("NEO4J_NAME")
# password = os.getenv("NEO4J_PASS")
# my_graph = Graph(uri, auth=(user, password))


# TODO: return
def get_all_lectures():
    result = App.graph.nodes.match("Lecture").all()
    return json.dumps([{"lecture": dict(row["lecture"])} for row in result])


# TODO: return
def get_by_name(name):
    result = App.graph.nodes.match("Lecture", name=name)
    return json.dumps({"Lecture": result})


# TODO: functionality
def get_by_course_name(name):
    Graph().nodes.match(name=name).first()
    result = App.graph.match(nodes=[name], r_type="IS_PART_OF_COURSE").all()
    return json.dumps([{"lecture": dict(row["lecture"])} for row in result])


# TODO: return
def delete_by_name(name):
    App.graph.delete("Lecture", name=name)


# TODO: functionality
def edit_lecture(name, editLecture: LectureUpdateSchema):
    title = editLecture.title
    description = editLecture.description
    index = editLecture.index
    lectureNode = App.graph.nodes.match("Lecture", name=name)
    tx = App.graph.begin()
    tx.run(
        "MATCH (l:Lecture) {name: $name} "
        "SET l.title: $title, l.description: $description, l.index: $index"
    )
    if(editLecture.courseName != None):
        lectureCourseRelShip = Relationship(lectureNode, "IS_PART_OF_COURSE", editLecture.courseName)
        tx.create(lectureCourseRelShip)
    if (editLecture.resourceName != None):
        lectureResourceRelShip = Relationship(lectureNode, "HAS_RESOURCE", editLecture.resourceName)
        tx.create(lectureResourceRelShip)
    tx.commit()


# TODO: functionality
def create_lecture(createLectureObject: LectureCreateSchema):
    lectureNode = Node("Lecture", id=createLectureObject.id, title=createLectureObject.title,
                       description=createLectureObject.description, index=createLectureObject.index)
    tx = App.graph.begin()
    tx.create(lectureNode)
    if (createLectureObject.courseName != None):
        lectureCourseRelShip = Relationship(lectureNode, "IS_PART_OF_COURSE", createLectureObject.courseName)
        tx.create(lectureCourseRelShip)
    if (createLectureObject.resourceName != None):
        lectureResourceRelShip = Relationship(lectureNode, "HAS_RESOURCE", createLectureObject.resourceName)
        tx.create(lectureResourceRelShip)
    tx.commit()
