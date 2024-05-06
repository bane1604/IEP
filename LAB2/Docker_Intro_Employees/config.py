import os

DATABASE_URL = "database" if ( "PRODUCTION" in os.environ ) else "localhost:3306"

class Configuration:
    SQLALCHEMY_DATABASE_URI = f"mysql://root:1234@{DATABASE_URL}/employees"