from py2neo import Graph, Node, Relationship
from fastapi import APIRouter, Path, Query, Body
import os
import json

from db.neo4jdb.resource import ResourceCreateSchema, ResourceUpdateSchema

# TODO: connection
uri = "neo4j+s://956e17de.databases.neo4j.io"
user = os.getenv("NEO4J_NAME")
password = os.getenv("NEO4J_PASS")
my_graph = Graph(uri, auth=(user, password))


# TODO: return
def get_all_resources():
    result = my_graph.nodes.match("Resource").all()
    return json.dumps([{"resource": dict(row["resource"])} for row in result])

# TODO: return
def get_by_name(name):
    result = my_graph.nodes.match("Resource", name=name)
    return json.dumps([{"resource": dict(row["resource"])} for row in result])

# TODO: return
def delete_by_name(name):
    result = my_graph.run(
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
    resourceNode = my_graph.nodes.match("Resource", name=name)
    resourceRelship = Relationship(resourceNode, "IS_FOR_LECTURE", editResource.lectureName)
    tx.create(resourceRelship)
    tx.commit()


# TODO: functionality
def create_resource(createResourceObject: ResourceCreateSchema):
    resourceNode = Node("Resource", title=createResourceObject.title,
                        description=createResourceObject.description, index=createResourceObject.index)
    resourceRelship = Relationship(resourceNode, "IS_FOR_LECTURE", createResourceObject.lectureName)
    tx = my_graph.begin()
    tx.create(resourceNode)
    tx.create(resourceRelship)
    tx.commit()
