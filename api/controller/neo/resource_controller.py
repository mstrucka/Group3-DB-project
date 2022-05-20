from bson import json_util
from py2neo import Graph, Node, Relationship
import json
from db.neo4jdb.resource import ResourceCreateSchema, ResourceUpdateSchema
from db.neo4jdb.neo import graph

# TODO: return
def get_all_resources():
    result = graph.nodes.match("Resource")
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        to_return.append(json_doc)
    return to_return

# TODO: return
def get_by_name(name):
    result = graph.nodes.match("Resource", name=name)
    return json.dumps([{"resource": dict(row["resource"])} for row in result])

# TODO: return
def delete_by_name(name):
    result = graph.run(
        "MATCH (r:Resource) {name: $name} "
        "DETACH DELETE r"
    )

# TODO: functionality, is name different than title? also, can be simplified
def edit_resource(name, editResource: ResourceUpdateSchema):
    title = editResource.title
    description = editResource.description
    index = editResource.index
    tx = Graph.begin()
    Graph().run(
        "MATCH (r:Resource) {name: $name} "
        "SET r.title: $title, r.description: $description, r.index: $index"
    )
    resourceNode = graph.nodes.match("Resource", name=name)
    resourceRelship = Relationship(resourceNode, "IS_FOR_LECTURE", editResource.lectureName)
    tx.create(resourceRelship)
    tx.commit()


# TODO: functionality
def create_resource(createResourceObject: ResourceCreateSchema):
    resourceNode = Node("Resource", title=createResourceObject.title,
                        description=createResourceObject.description, index=createResourceObject.index)
    resourceRelship = Relationship(resourceNode, "IS_FOR_LECTURE", createResourceObject.lectureName)
    tx = graph.begin()
    tx.create(resourceNode)
    tx.create(resourceRelship)
    tx.commit()
