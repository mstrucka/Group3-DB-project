import datetime
from py2neo import Node, Relationship
import json
from db.neo4jdb.payment import PaymentCreateSchema
from db.neo4jdb.neo import graph


def get_all_payments():
    result = graph.nodes.match("Payment")
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=str)
        to_return.append(json_doc)
    return to_return


def get_by_id(id):
    result = graph.nodes.match("Payment", id=id).first()
    return json.dumps(result, default=str)


# TODO: return?
def delete_by_id(id):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Payment", id=id).first()
    tx.delete(nodeToDelete)
    tx.commit()


# TODO: works, return!
def create_payment(createPaymentObject: PaymentCreateSchema):
    paymentNode = Node("Payment", id=createPaymentObject.id,
                       date=datetime.date.today(), price=createPaymentObject.price)
    tx = graph.begin()
    tx.create(paymentNode)
    studentNode = graph.nodes.match("Student", name=createPaymentObject.studentName).first()
    if createPaymentObject.courseName is not None:
        enroll(studentNode, createPaymentObject.courseName)
    if createPaymentObject.studentName is not None:
        paymentRelship = Relationship(paymentNode, "MADE_BY", studentNode)
        tx.create(paymentRelship)
    tx.commit()

def enroll(studentNode, courseName):
    courseNode = graph.nodes.match("Course", title=courseName).first()
    studentRelship = Relationship(studentNode, "IS_ENROLLED_IN_COURSE", courseNode)
    graph.create(studentRelship)
