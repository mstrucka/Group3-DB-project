from bson import json_util
from py2neo import Node, Relationship
import json
from db.neo4jdb.course import CourseCreate, CourseUpdate
from db.neo4jdb.neo import graph


def get_all_courses():
    result = graph.nodes.match("Course")
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        to_return.append(json_doc)
    return to_return


def get_all_enrolled_students(name):
    query = f'MATCH (c:Course {{name: "{name}"}})<-[:IS_ENROLLED_IN_COURSE]-(s:Student) return s.name'
    result = graph.run(query)
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        to_return.append(json_doc)
    return to_return


def get_by_name(name):
    result = graph.nodes.match("Course", name=name).first()
    return json.dumps(result, default=json_util.default)


def delete_by_name(name):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Course", name=name).first()
    result = tx.delete(nodeToDelete)
    tx.commit()
    if result is None:
        return True


def edit_course(name, course: CourseUpdate):
    onSale = course.onSale
    description = course.description
    level = course.level
    price = course.price
    isCoD = course.isCourseOfTheDay
    tx = graph.begin()
    tx.run(
        f'MATCH (c:Course {{name: "{name}"}}) SET c.description= "{description}", c.onSale= {onSale}, c.level= {level},'
        f' c.price= {price}, c.isCourseOfTheDay= {isCoD} '
    )
    if course.lectureName is not None:
        graph.run(
            f'MATCH (c:Course {{name: "{name}"}}), (l:Lecture {{name: "{course.lectureName}"}}) CREATE (c)-[r:HAS_LECTURE]->(l)')
    if course.teacherName is not None:
        graph.run(
            f'MATCH (c:Course {{name: "{name}"}}), (t:Teacher {{name: "{course.teacherName}"}}) CREATE (c)-[r:TAUGHT_BY]->(t)')
    result = tx.commit()
    if result is None:
        return True


def create_course(course: CourseCreate):
    courseNode = Node("Course", name=course.name, description=course.description,
                      level=course.level, onSale=course.onSale,
                      isCourseOfTheDay=course.isCourseOfTheDay)
    tx = graph.begin()
    tx.create(courseNode)
    if course.lectureName is not None:
        lectureNode = graph.nodes.match("Lecture", name=course.lectureName).first()
        lectureCourseRelShip = Relationship(courseNode, "HAS_LECTURE", lectureNode)
        tx.create(lectureCourseRelShip)
    if course.teacherName is not None:
        teacherNode = graph.nodes.match("Teacher", name=course.teacherName).first()
        CourseTeacherRelship = Relationship(courseNode, "IS_TAUGHT_BY", teacherNode)
        tx.create(CourseTeacherRelship)
    result = tx.commit()
    if result is None:
        return True
