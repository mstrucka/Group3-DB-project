from bson import json_util
from py2neo import Node, Relationship
import json
from db.neo4jdb.payment import PaymentCreateSchema
from db.neo4jdb.neo import graph

# TODO: return
def get_all_payments():
    result = graph.nodes.match("Payment")
    to_return = []
    for doc in result:
        json_doc = json.dumps(doc, default=str)
        to_return.append(json_doc)
    return to_return

# TODO: return
def get_by_id(id):
    result = graph.nodes.match("Payment", id=id)
    return json.dumps({"payment": result})

# TODO: return
def delete_by_id(id):
    result = graph.run(
        "MATCH (p:Payment) {id: $id} "
        "DETACH DELETE p"
    )

# TODO: functionality
def create_payment(createPaymentObject: PaymentCreateSchema):
    paymentNode = Node("Payment", id=createPaymentObject.id,
                        date=createPaymentObject.date, price=createPaymentObject.price)
    paymentRelship = Relationship(paymentNode, "MADE_BY", createPaymentObject.studentName)
    studentNode = graph.nodes.match("Student", name=createPaymentObject.studentName)
    studentRelship = Relationship(studentNode, "IS_ENROLLED_IN_COURSE", createPaymentObject.courseName)
    tx = graph.begin()
    tx.create(paymentNode)
    tx.create(paymentRelship)
    tx.create(studentRelship)
    tx.commit()
