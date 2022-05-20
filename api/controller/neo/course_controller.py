from py2neo import Node, Relationship
import json
from db.neo4jdb.course import CourseCreateSchema, CourseUpdateSchema
from db.neo4jdb.neo import graph

# TODO: return
def get_all_courses():
    result = graph.nodes.match("Course").all()
    return json.dumps([{"course": dict(row["course"])} for row in result])


# TODO: return
def get_by_name(name):
    result = graph.nodes.match("Course", name=name)
    print(result)
    return json.dumps({"Course": result.__dict__})


# TODO: functionality
def get_by_course_name(name):
    graph.nodes.match(name=name).first()
    result = graph.match(nodes=[name], r_type="IS_PART_OF_COURSE").all()
    return json.dumps([{"lecture": dict(row["lecture"])} for row in result])


# TODO: return
def delete_by_name(name):
    graph.delete("Course", name=name)


# TODO: functionality
def edit_course(name, editCourse: CourseUpdateSchema):
    onSale = editCourse.onSale
    description = editCourse.description
    level = editCourse.level
    price = editCourse.price
    isCoD = editCourse.isCourseOfTheDay
    courseNode = graph.nodes.match("Course", name=name)
    tx = graph.begin()
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
    tx = graph.begin()
    tx.create(courseNode)
    if (course.lectureName != None):
        lectureCourseRelShip = Relationship(courseNode, "HAS_LECTURE", course.lectureName)
        tx.create(lectureCourseRelShip)
    if (course.teacherName != None):
        CourseTeacherRelship = Relationship(courseNode, "IS_TAUGHT_BY", course.teacherName)
        tx.create(CourseTeacherRelship)
    tx.commit()
