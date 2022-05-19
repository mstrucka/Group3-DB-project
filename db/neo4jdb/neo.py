from neo4j import GraphDatabase
import os

from py2neo import Graph


class App:
    # uri = os.getenv("NEO4J_URI")
    uri = "neo4j+s://956e17de.databases.neo4j.io"
    user = os.getenv("NEO4J_NAME")
    password = os.getenv("NEO4J_PASS")
    graph = Graph(uri, auth=(user, password))

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_nodes_and_relationships(self):
        with self.driver.session() as session:
            with open('creation_script.txt') as file:
                query = file.read()
                session.execute(query)


# if __name__ == "__main__":
#     uri = os.getenv("NEO4J_URI")
#     user = os.getenv("NEO4J_NAME")
#     password = os.getenv("NEO4J_PASS")
#     app = App(uri, user, password)
#     app.close()
