from sqlalchemy import create_engine, text
engine = create_engine('mysql+mysqldb://root:root@localhost/mydb', echo=True, future=True)

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())