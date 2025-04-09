import snowflake.connector
import json

def get_connection():
    with open("config.json") as f:
        creds = json.load(f)

    conn = snowflake.connector.connect(
        user=creds["user"],
        password=creds["password"],
        account=creds["account"],
        warehouse=creds["warehouse"],
        database=creds["database"],
        schema=creds["schema"],
        role=creds["role"]
    )
    return conn
