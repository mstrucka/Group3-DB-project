from py2neo import Graph, Node, Relationship
import os
import json

from db.neo4jdb.course import CourseCreateSchema, CourseUpdateSchema


# TODO: connection
# uri = os.getenv("NEO4J_URI")
# user = os.getenv("NEO4J_NAME")
# password = os.getenv("NEO4J_PASS")
# my_graph = Graph(uri, auth=(user, password))


# TODO: return
def get_all_courses():
    result = Graph().nodes.match("Course").all()
    return json.dumps([{"course": dict(row["course"])} for row in result])


# TODO: return
def get_by_name(name):
    result = Graph().nodes.match("Course", name=name)
    return json.dumps({"Course": result})


# TODO: functionality
def get_by_course_name(name):
    Graph().nodes.match(name=name).first()
    result = Graph().match(nodes=[name], r_type="IS_PART_OF_COURSE").all()
    return json.dumps([{"lecture": dict(row["lecture"])} for row in result])


# TODO: return
def delete_by_name(name):
    Graph().delete("Course", name=name)


# TODO: functionality
def edit_course(name, editCourse: CourseUpdateSchema):
    onSale = editCourse.onSale
    description = editCourse.description
    level = editCourse.level
    price = editCourse.price
    isCoD = editCourse.isCourseOfTheDay
    courseNode = Graph().nodes.match("Course", name=name)
    tx = Graph().begin()
    tx.run(
        "MATCH (c:Course) {name: $name} "
        "SET c.level: $level, c.description: $description, c.onSale: $onSale, "
        "c.price: $price, c.isCourseOfTheDay: $isCoD"
    )
    if (editCourse.lectureName != None):
        lectureCourseRelShip = Relationship(courseNode, "HAS_LECTURE", editCourse.lectureName)
        tx.create(lectureCourseRelShip)
    if (editCourse.teacherName != None):
        CourseTeacherRelship = Relationship(courseNode, "IS_TAUGHT_BY", editCourse.teacherName)
        tx.create(CourseTeacherRelship)
    tx.commit()


# TODO: functionality
def create_lecture(course: CourseCreateSchema):
    courseNode = Node("Course", id=course.id, title=course.title,
                      description=course.description, level=course.level, onSale=course.onSale,
                      isCourseOfTheDay=course.isCourseOfTheDay)
    tx = Graph().begin()
    tx.create(courseNode)
    if (course.lectureName != None):
        lectureCourseRelShip = Relationship(courseNode, "HAS_LECTURE", course.lectureName)
        tx.create(lectureCourseRelShip)
    if (course.teacherName != None):
        CourseTeacherRelship = Relationship(courseNode, "IS_TAUGHT_BY", course.teacherName)
        tx.create(CourseTeacherRelship)
    tx.commit()
