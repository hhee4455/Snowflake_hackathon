import streamlit as st
from snowflake.snowpark import Session
import snowflake.connector

def get_snowflake_connection():
    """
    Snowflake connector.connect() 방식 - cursor 또는 SQL 직접 실행에 사용
    """
    config = st.secrets["snowflake"]

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

def get_snowpark_session():
    """
    Snowpark Session 객체 생성 - DataFrame API, .sql() 등 사용 시 필요
    """
    config = st.secrets["snowflake"]

    session = Session.builder.configs({
        "account": config["account"],
        "user": config["user"],
        "password": config["password"],
        "role": config["role"],
        "warehouse": config["warehouse"],
        "database": config["database"],
        "schema": config["schema"]
    }).create()

    return session
