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


def get_by_title(title):
    result = graph.nodes.match("Course", title=title).first()
    return json.dumps(result, default=json_util.default)


# TODO: still does not work
def get_by_course_title(title):
    result = graph.nodes.match("Course", title=title, r_type="IS_PART_OF_COURSE")
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        to_return.append(json_doc)
    return to_return


def delete_by_title(title):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Course", title=title).first()
    result = tx.delete(nodeToDelete)
    tx.commit()
    if result is None:
        return True


# TODO: still does not work
def edit_course(title, editCourse: CourseUpdate):
    onSale = editCourse.onSale
    description = editCourse.description
    level = editCourse.level
    price = editCourse.price
    isCoD = editCourse.isCourseOfTheDay
    tx = graph.begin()
    tx.run(
        f'MATCH (c:Course {{title: "{title}"}}) SET c.description= "{description}", c.onSale= {onSale}, c.level= {level},'
        f' c.price= {price}, c.isCourseOfTheDay= {isCoD} '
    )
    courseNode = graph.nodes.match("Course", title=title)
    if editCourse.lectureName is not None:
        lectureNode = graph.nodes.match("Lecture", title=editCourse.lectureName).first()
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
    courseNode = Node("Course", title=course.title, description=course.description,
                      level=course.level, onSale=course.onSale,
                      isCourseOfTheDay=course.isCourseOfTheDay)
    tx = graph.begin()
    tx.create(courseNode)
    if course.lectureName is not None:
        lectureNode = graph.nodes.match("Lecture", title=course.lectureName).first()
        lectureCourseRelShip = Relationship(courseNode, "HAS_LECTURE", lectureNode)
        tx.create(lectureCourseRelShip)
    if course.teacherName is not None:
        teacherNode = graph.nodes.match("Teacher", name=course.teacherName).first()
        CourseTeacherRelship = Relationship(courseNode, "IS_TAUGHT_BY", teacherNode)
        tx.create(CourseTeacherRelship)
    result = tx.commit()
    if result is None:
        return True
