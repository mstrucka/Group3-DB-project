from bson import json_util
from py2neo import Node, Relationship
import json
import http.client
from db.neo4jdb.resource import ResourceCreateSchema, ResourceUpdateSchema
from db.neo4jdb.neo import graph

def get_all_resources():
    result = graph.nodes.match("Resource")
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        to_return.append(json_doc)
    return to_return

def get_by_name(name):
    result = graph.nodes.match("Resource", name=name).first()
    return json.dumps(result, default=json_util.default)

# TODO: return?
def delete_by_name(name):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Resource", name=name).first()
    tx.delete(nodeToDelete)
    tx.commit()

# TODO: relationship
def edit_resource(name, editResource: ResourceUpdateSchema):
    tx = graph.begin()
    if editResource.uri is not None:
        uri = editResource.uri
        result = tx.run(
            f'MATCH (r:Resource {{name: "{name}"}}) SET r.uri= "{uri}"'
        )
        return result.stats()
    elif editResource.lectureName is not None:
        resourceNode = graph.nodes.match("Resource", name=name)
        resourceRelship = Relationship(resourceNode, "IS_FOR_LECTURE", editResource.lectureName)
        tx.create(resourceRelship)
        tx.commit()
    else:
        return http.client.responses[http.client.BAD_REQUEST]

# TODO: works, return only
def create_resource(createResourceObject: ResourceCreateSchema):
    resourceNode = Node("Resource", id=createResourceObject.id,
                        name=createResourceObject.name, uri=createResourceObject.uri)
    tx = graph.begin()
    tx.create(resourceNode)
    if createResourceObject.lectureName is not None:
        lectureNode = graph.nodes.match("Lecture", title=createResourceObject.lectureName).first()
        resourceRelship = Relationship(resourceNode, "IS_FOR_LECTURE", lectureNode)
        tx.create(resourceRelship)
    tx.commit()
