from py2neo import Graph, Node, Relationship
import os
import json
from db.neo4jdb.payment import PaymentCreateSchema


# TODO: connection
# uri = "neo4j+s://956e17de.databases.neo4j.io"
# user = os.getenv("NEO4J_NAME")
# password = os.getenv("NEO4J_PASS")
# my_graph = Graph(uri, auth=(user, password))


# TODO: return
def get_all_payments():
    result = Graph().nodes.match("Payment").all()
    return json.dumps([{"payment": dict(row["payment"])} for row in result])

# TODO: return
def get_by_id(id):
    result = Graph().nodes.match("Payment", id=id)
    return json.dumps({"payment": result})

# TODO: return
def delete_by_id(id):
    result = Graph().run(
        "MATCH (p:Payment) {id: $id} "
        "DETACH DELETE p"
    )

# TODO: functionality
def create_payment(createPaymentObject: PaymentCreateSchema):
    paymentNode = Node("Payment", id=createPaymentObject.id,
                        date=createPaymentObject.date, price=createPaymentObject.price)
    paymentRelship = Relationship(paymentNode, "MADE_BY", createPaymentObject.studentName)
    studentNode = Graph().nodes.match("Student", name=createPaymentObject.studentName)
    studentRelship = Relationship(studentNode, "IS_ENROLLED_IN_COURSE", createPaymentObject.courseName)
    tx = Graph().begin()
    tx.create(paymentNode)
    tx.create(paymentRelship)
    tx.create(studentRelship)
    tx.commit()
