from bson import json_util
from py2neo import Node, Relationship
import json
from db.neo4jdb.neo import graph
from db.neo4jdb.lecture import LectureCreateSchema, LectureUpdateSchema

# TODO: return
def get_all_lectures():
    result = graph.nodes.match("Lecture")
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        to_return.append(json_doc)
    return to_return


# TODO: return
def get_by_name(name):
    result = graph.nodes.match("Lecture", name=name)
    return json.dumps({"Lecture": result})


# TODO: functionality
def get_by_course_name(name):
    graph.nodes.match(name=name).first()
    result = graph.match(nodes=[name], r_type="IS_PART_OF_COURSE").all()
    return json.dumps([{"lecture": dict(row["lecture"])} for row in result])


# TODO: return
def delete_by_name(name):
    graph.delete("Lecture", name=name)


# TODO: functionality
def edit_lecture(name, editLecture: LectureUpdateSchema):
    title = editLecture.title
    description = editLecture.description
    index = editLecture.index
    lectureNode = graph.nodes.match("Lecture", name=name)
    tx = graph.begin()
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
    tx = graph.begin()
    tx.create(lectureNode)
    if (createLectureObject.courseName != None):
        lectureCourseRelShip = Relationship(lectureNode, "IS_PART_OF_COURSE", createLectureObject.courseName)
        tx.create(lectureCourseRelShip)
    if (createLectureObject.resourceName != None):
        lectureResourceRelShip = Relationship(lectureNode, "HAS_RESOURCE", createLectureObject.resourceName)
        tx.create(lectureResourceRelShip)
    tx.commit()
