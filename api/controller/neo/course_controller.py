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


def get_by_name(name):
    result = graph.nodes.match("Course", name=name).first()
    return json.dumps(result, default=json_util.default)


def get_by_course_name(name):
    query = f'MATCH (c:Course {{name: "{name}"}})-[:HAS_LECTURE]->(lecture) return lecture.name'
    result = graph.run(query)
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        to_return.append(json_doc)
    return to_return


def delete_by_name(name):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Course", name=name).first()
    result = tx.delete(nodeToDelete)
    tx.commit()
    if result is None:
        return True


# TODO: still does not work
def edit_course(name, editCourse: CourseUpdate):
    onSale = editCourse.onSale
    description = editCourse.description
    level = editCourse.level
    price = editCourse.price
    isCoD = editCourse.isCourseOfTheDay
    tx = graph.begin()
    tx.run(
        f'MATCH (c:Course {{name: "{name}"}}) SET c.description= "{description}", c.onSale= {onSale}, c.level= {level},'
        f' c.price= {price}, c.isCourseOfTheDay= {isCoD} '
    )
    courseNode = graph.nodes.match("Course", name=name)
    if editCourse.lectureName is not None:
        lectureNode = graph.nodes.match("Lecture", name=editCourse.lectureName).first()
        lectureCourseRelShip = Relationship(courseNode, "HAS_LECTURE", lectureNode)
        tx.create(lectureCourseRelShip)
    if editCourse.teacherName is not None:
        teacherNode = graph.nodes.match("Teacher", name=editCourse.teacherName).first()
        CourseTeacherRelship = Relationship(teacherNode, "TEACHES", courseNode)
        tx.create(CourseTeacherRelship)
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
