from py2neo import Node, Relationship
import json
from db.neo4jdb.payment import PaymentCreateSchema
from db.neo4jdb.neo import graph

# TODO: return
def get_all_payments():
    result = graph.nodes.match("Payment").all()
    return json.dumps([{"payment": dict(row["payment"])} for row in result])

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
