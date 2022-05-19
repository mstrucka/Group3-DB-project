from neo4j import GraphDatabase
import os
from py2neo import Graph

uri = os.getenv('NEO4J_URI')
user = os.getenv("NEO4J_NAME")
password = os.getenv("NEO4J_PASS")
driver = GraphDatabase.driver(uri, auth=(user, password))
graph = Graph(uri, auth=(user, password), secure=True)

def create_nodes_and_relationships(driver):
    with driver.session() as session:
        with open('creation_script.txt') as file:
            query = file.read()
            session.execute(query)
