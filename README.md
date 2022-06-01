# Group3-DB-project

## Install dependencies
Python version must be >= 3.10.2

Install dependencies with pip install -r requirements.txt

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
