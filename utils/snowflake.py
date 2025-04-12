import snowflake.connector
import json

def get_snowflake_connection(config_path="config.json"):
    with open(config_path) as f:
        config = json.load(f)["snowflake"]

    conn = snowflake.connector.connect(
        user=config["user"],
        password=config["password"],
        account=config["account"],
        warehouse=config["warehouse"],
        database=config["database"],
        schema=config["schema"],
        role=config["role"]
    )
    return conn
