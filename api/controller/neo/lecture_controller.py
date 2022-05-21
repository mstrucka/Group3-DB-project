from bson import json_util
from py2neo import Node, Relationship
import json
from db.neo4jdb.neo import graph
from db.neo4jdb.lecture import LectureCreateSchema, LectureUpdateSchema

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

# TODO: functionality
def get_by_course_title(title):
    graph.nodes.match(title=title).first()
    result = graph.match(nodes=[title], r_type="IS_PART_OF_COURSE").all()
    return json.dumps([{"lecture": dict(row["lecture"])} for row in result])


# TODO: return
def delete_by_title(title):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Lecture", title=title).first()
    tx.delete(nodeToDelete)
    tx.commit()


# TODO: relationships, return
def edit_lecture(title, editLecture: LectureUpdateSchema):
    description = editLecture.description
    index = editLecture.index
    lectureNode = graph.nodes.match("Lecture", title=title)
    tx = graph.begin()
    tx.run(
        f'MATCH (l:Lecture {{title: "{title}"}}) SET l.description= "{description}", l.index= {index}'
    )
    if(editLecture.courseName != None):
        lectureCourseRelShip = Relationship(lectureNode, "IS_PART_OF_COURSE", editLecture.courseName)
        tx.create(lectureCourseRelShip)
    if (editLecture.resourceName != None):
        lectureResourceRelShip = Relationship(lectureNode, "HAS_RESOURCE", editLecture.resourceName)
        tx.create(lectureResourceRelShip)
    tx.commit()


# TODO: works, return only
def create_lecture(createLectureObject: LectureCreateSchema):
    lectureNode = Node("Lecture", title=createLectureObject.title,
                       description=createLectureObject.description, index=createLectureObject.index)
    tx = graph.begin()
    tx.create(lectureNode)
    if (createLectureObject.courseName != None):
        courseNode = graph.nodes.match("Course", title=createLectureObject.courseName).first()
        lectureCourseRelShip = Relationship(lectureNode, "IS_PART_OF_COURSE", courseNode)
        tx.create(lectureCourseRelShip)
    if (createLectureObject.resourceName != None):
        resourceNode = graph.nodes.match("Resource", name=createLectureObject.resourceName).first()
        lectureResourceRelShip = Relationship(lectureNode, "HAS_RESOURCE", resourceNode)
        tx.create(lectureResourceRelShip)
    tx.commit()
