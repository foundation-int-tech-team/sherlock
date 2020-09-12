from os import environ

import queries
from dotenv import load_dotenv


load_dotenv()

URI = queries.uri(
    host=environ['PG_HOST'],
    port=environ['PG_PORT'],
    dbname=environ['PG_DBNAME'],
    user=environ['PG_USER'],
    password=environ['PG_PASSWORD']
)


def get_session():
    return queries.Session(URI)
