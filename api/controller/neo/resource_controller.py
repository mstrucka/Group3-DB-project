from bson import json_util
from py2neo import Node, Relationship
import json
from db.neo4jdb.resource import ResourceCreate, ResourceUpdate
from db.neo4jdb.neo import graph


def get_all_resources():
    result = graph.nodes.match("Resource")
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        to_return.append(json_doc)
    return to_return


def get_all_resources_for_lecture_names(lectureName):
    query = f'MATCH (l:Lecture {{name: "{lectureName}"}})-[:HAS_RESOURCE]->(r:Resource) return r.name'
    result = graph.run(query)
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        to_return.append(json_doc)
    return to_return


def get_all_resources_for_lecture_full(lectureName):
    query = f'MATCH (l:Lecture {{name: "{lectureName}"}})-[:HAS_RESOURCE]->(r:Resource) return r'
    result = graph.run(query)
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        to_return.append(json_doc)
    return to_return


def get_by_name(name):
    result = graph.nodes.match("Resource", name=name).first()
    return json.dumps(result, default=json_util.default)


def delete_by_name(name):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Resource", name=name).first()
    tx.delete(nodeToDelete)
    result = tx.commit()
    if result is None:
        return True


def edit_resource(name, resource: ResourceUpdate):
    tx = graph.begin()
    if resource.uri is not None:
        uri = resource.uri
        result = tx.run(
            f'MATCH (r:Resource {{name: "{name}"}}) SET r.uri= "{uri}"'
        )
        return result.stats()
    elif resource.lectureName is not None:
        graph.run(
            f'MATCH (l:Lecture {{name: "{resource.lectureName}"}}), (r:Resource {{name: "{name}"}}) CREATE (l)-[r:HAS_RESOURCE]->(r)')
    result = tx.commit()
    if result is None:
        return True


def create_resource(resource: ResourceCreate):
    resourceNode = Node("Resource", name=resource.name, uri=resource.uri)
    tx = graph.begin()
    tx.create(resourceNode)
    if resource.lectureName is not None:
        lectureNode = graph.nodes.match("Lecture", name=resource.lectureName).first()
        resourceRelship = Relationship(resourceNode, "IS_FOR_LECTURE", lectureNode)
        tx.create(resourceRelship)
    result = tx.commit()
    if result is None:
        return True
