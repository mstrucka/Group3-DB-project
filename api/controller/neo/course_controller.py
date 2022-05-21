from bson import json_util
from py2neo import Node, Relationship
import json
from db.neo4jdb.course import CourseCreateSchema, CourseUpdateSchema
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


# TODO: functionality
def get_by_course_title(title):
    courseNode = graph.nodes.match("Course", title=title).first()
    result = graph.match(courseNode, r_type="IS_PART_OF_COURSE")
    return json.dumps(result, default=json_util.default)


# TODO: return
def delete_by_title(title):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Course", title=title).first()
    tx.delete(nodeToDelete)
    tx.commit()


# TODO: relationships, return
def edit_course(title, editCourse: CourseUpdateSchema):
    onSale = editCourse.onSale
    description = editCourse.description
    level = editCourse.level
    price = editCourse.price
    isCoD = editCourse.isCourseOfTheDay
    courseNode = graph.nodes.match("Course", title=title)
    tx = graph.begin()
    tx.run(
        f'MATCH (c:Course {{title: "{title}"}}) SET c.description= "{description}", c.onSale= {onSale}, c.level= {level},'
        f' c.price= {price}, c.isCourseOfTheDay= {isCoD} '
    )
    if (editCourse.lectureName != None):
        lectureCourseRelShip = Relationship(courseNode, "HAS_LECTURE", editCourse.lectureName)
        tx.create(lectureCourseRelShip)
    if (editCourse.teacherName != None):
        CourseTeacherRelship = Relationship(courseNode, "IS_TAUGHT_BY", editCourse.teacherName)
        tx.create(CourseTeacherRelship)
    tx.commit()

# TODO: works, return only
def create_course(course: CourseCreateSchema):
    courseNode = Node("Course", id=course.id, title=course.title,
                      description=course.description, level=course.level, onSale=course.onSale,
                      isCourseOfTheDay=course.isCourseOfTheDay)
    tx = graph.begin()
    tx.create(courseNode)
    if (course.lectureName != None):
        lectureNode = graph.nodes.match("Lecture", title=course.lectureName).first()
        lectureCourseRelShip = Relationship(courseNode, "HAS_LECTURE", lectureNode)
        tx.create(lectureCourseRelShip)
    if (course.teacherName != None):
        teacherNode = graph.nodes.match("Teacher", name=course.teacherName).first()
        CourseTeacherRelship = Relationship(courseNode, "IS_TAUGHT_BY", teacherNode)
        tx.create(CourseTeacherRelship)
    tx.commit()
