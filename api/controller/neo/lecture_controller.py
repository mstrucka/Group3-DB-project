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


def get_by_title(title):
    result = graph.nodes.match("Lecture", title=title).first()
    return json.dumps(result, default=json_util.default)


# TODO: still does not work
def get_by_course_title(title):
    graph.nodes.match(title=title).first()
    result = graph.match(nodes=[title], r_type="IS_PART_OF_COURSE").all()
    return json.dumps([{"lecture": dict(row["lecture"])} for row in result])


def delete_by_title(title):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Lecture", title=title).first()
    tx.delete(nodeToDelete)
    result = tx.commit()
    if result is None:
        return True


# TODO: still does not work
def edit_lecture(title, lecture: LectureUpdate):
    description = lecture.description
    index = lecture.index
    lectureNode = graph.nodes.match("Lecture", title=title)
    tx = graph.begin()
    tx.run(
        f'MATCH (l:Lecture {{title: "{title}"}}) SET l.description= "{description}", l.index= {index}'
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
    lectureNode = Node("Lecture", title=lecture.title,
                       description=lecture.description, index=lecture.index)
    tx = graph.begin()
    tx.create(lectureNode)
    if lecture.courseName is not None:
        courseNode = graph.nodes.match("Course", title=lecture.courseName).first()
        lectureCourseRelShip = Relationship(lectureNode, "IS_PART_OF_COURSE", courseNode)
        tx.create(lectureCourseRelShip)
    if lecture.resourceName is not None:
        resourceNode = graph.nodes.match("Resource", name=lecture.resourceName).first()
        lectureResourceRelShip = Relationship(lectureNode, "HAS_RESOURCE", resourceNode)
        tx.create(lectureResourceRelShip)
    result = tx.commit()
    if result is None:
        return True
