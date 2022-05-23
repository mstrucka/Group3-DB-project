# Group3-DB-project

## Installation procedure
Since the database is a MySQL database, you need to have MySQL installed and running on your computer.

Then you need to do the following steps:
- Run ‘ddl-script.sql’ to create the schema and tables.
- Run the scripts with stored objects (routines.sql, events.sql, triggers.sql, views.sql) in any order.
- Run ‘data-inserts.sql’, in order to populate the database.

After completion of these steps, your setup is finished.

## How to run server
Server is run with FastAPI

Make sure to add your local db settings to .env file. See .env-example for reference.

Locally:
Run the following command: uvicorn main:app --reload

Default port is 8000

## API's

Application consists of 3 API's, one for each DB paradigm.
They each live as a separate app mounted on the main app.

Root paths
- MySQL: /api/v1/mysql
- MongoDB: /api/v1/mongo
- Neo4j: /api/v1/neo4j

### Docs

Swagger/OpenAPI interactive docs are auto-generated. Go to /docs to access it.
