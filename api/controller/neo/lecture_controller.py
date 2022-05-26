from bson import json_util
from py2neo import Node, Relationship
import json
from db.neo4jdb.neo import graph
from db.neo4jdb.lecture import LectureCreate, LectureUpdate


def get_all_lectures():
    result = graph.nodes.match("Lecture")
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        to_return.append(json_doc)
    return to_return


def get_by_name(name):
    result = graph.nodes.match("Lecture", name=name).first()
    return json.dumps(result, default=json_util.default)


def delete_by_name(name):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Lecture", name=name).first()
    tx.delete(nodeToDelete)
    result = tx.commit()
    if result is None:
        return True


# TODO: still does not work
def edit_lecture(name, lecture: LectureUpdate):
    description = lecture.description
    index = lecture.index
    lectureNode = graph.nodes.match("Lecture", name=name)
    tx = graph.begin()
    tx.run(
        f'MATCH (l:Lecture {{name: "{name}"}}) SET l.description= "{description}", l.index= {index}'
    )
    if lecture.courseName is not None:
        lectureCourseRelShip = Relationship(lectureNode, "IS_PART_OF_COURSE", lecture.courseName)
        tx.create(lectureCourseRelShip)
    if lecture.resourceName is not None:
        lectureResourceRelShip = Relationship(lectureNode, "HAS_RESOURCE", lecture.resourceName)
        tx.create(lectureResourceRelShip)
    result = tx.commit()
    if result is None:
        return True


def create_lecture(lecture: LectureCreate):
    lectureNode = Node("Lecture", name=lecture.name,
                       description=lecture.description, index=lecture.index)
    tx = graph.begin()
    tx.create(lectureNode)
    if lecture.courseName is not None:
        courseNode = graph.nodes.match("Course", name=lecture.courseName).first()
        lectureCourseRelShip = Relationship(lectureNode, "IS_PART_OF_COURSE", courseNode)
        tx.create(lectureCourseRelShip)
    if lecture.resourceName is not None:
        resourceNode = graph.nodes.match("Resource", name=lecture.resourceName).first()
        lectureResourceRelShip = Relationship(lectureNode, "HAS_RESOURCE", resourceNode)
        tx.create(lectureResourceRelShip)
    result = tx.commit()
    if result is None:
        return True
