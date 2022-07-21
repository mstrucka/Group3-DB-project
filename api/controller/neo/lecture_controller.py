from bson import json_util
from py2neo import Node, Relationship
import json
from db.neo4jdb.neo import graph
from db.neo4jdb.lecture import LectureCreate, LectureUpdate


def get_all_lectures():
    result = graph.nodes.match("Lecture").all()
    return result


def get_by_name(name):
    result = graph.nodes.match("Lecture", name=name).first()
    return result


def get_all_lectures_for_course_names(courseName):
    query = f'MATCH (c:Course {{name: "{courseName}"}})-[:HAS_LECTURE]->(l:Lecture) return l.name'
    result = graph.run(query).data()
    return result


def get_all_lectures_for_course_full(courseName):
    query = f'MATCH (c:Course {{name: "{courseName}"}})-[:HAS_LECTURE]->(l:Lecture) return l'
    result = graph.run(query).data()
    return result


def delete_by_name(name):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Lecture", name=name).first()
    tx.delete(nodeToDelete)
    result = tx.commit()
    if result is None:
        return True


def edit_lecture(name, lecture: LectureUpdate):
    description = lecture.description
    index = lecture.index
    tx = graph.begin()
    tx.run(
        f'MATCH (l:Lecture {{name: "{name}"}}) SET l.description= "{description}", l.index= {index}'
    )
    if lecture.courseName is not None:
        graph.run(
            f'MATCH (c:Course {{name: "{lecture.courseName}"}}), (l:Lecture {{name: "{name}"}}) CREATE (c)-[r:HAS_LECTURE]->(l)')
    if lecture.resourceName is not None:
        graph.run(
            f'MATCH (r:Resource {{name: "{lecture.resourceName}"}}), (l:Lecture {{name: "{name}"}}) CREATE (l)-[r:HAS_RESOURCE]->(r)')
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
        lectureCourseRelShip = Relationship(courseNode, "HAS_LECTURE", lectureNode)
        tx.create(lectureCourseRelShip)
    if lecture.resourceName is not None:
        resourceNode = graph.nodes.match("Resource", name=lecture.resourceName).first()
        lectureResourceRelShip = Relationship(lectureNode, "HAS_RESOURCE", resourceNode)
        tx.create(lectureResourceRelShip)
    result = tx.commit()
    if result is None:
        return True
