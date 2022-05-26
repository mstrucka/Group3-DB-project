import datetime
from py2neo import Node, Relationship
import json
from db.neo4jdb.payment import PaymentCreate
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


def delete_by_id(id):
    tx = graph.begin()
    nodeToDelete = graph.nodes.match("Payment", id=id).first()
    result = tx.delete(nodeToDelete)
    tx.commit()
    if result is None:
        return True


def create_payment(payment: PaymentCreate):
    paymentNode = Node("Payment", id=payment.id,
                       date=datetime.date.today(), price=payment.price)
    tx = graph.begin()
    tx.create(paymentNode)
    studentNode = graph.nodes.match("Student", name=payment.studentName).first()
    if payment.courseName is not None:
        enroll(studentNode, payment.courseName)
    if payment.studentName is not None:
        paymentRelship = Relationship(paymentNode, "MADE_BY", studentNode)
        tx.create(paymentRelship)
    result = tx.commit()
    if result is None:
        return True


def enroll(studentNode, courseName):
    courseNode = graph.nodes.match("Course", name=courseName).first()
    studentRelship = Relationship(studentNode, "IS_ENROLLED_IN_COURSE", courseNode)
    graph.create(studentRelship)
