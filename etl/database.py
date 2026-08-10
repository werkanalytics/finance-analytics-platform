from sqlalchemy import create_engine

def get_engine():
    return create_engine(
        "postgresql+psycopg2://postgres:ahmet2908@host.docker.internal:5432/postgres"
    )