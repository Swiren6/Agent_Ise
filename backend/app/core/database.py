from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import mysql.connector
from .config import settings

class DatabaseManager:
    def __init__(self):
        self.db = None
        self._engine = None
        
    def get_database(self) -> SQLDatabase:
        if self.db is None:
            self.db = SQLDatabase.from_uri(
                settings.database_url,
                sample_rows_in_table_info=0,
                engine_args={"pool_timeout": 30, "pool_recycle": 3600}
            )
        return self.db
        
    def test_connection(self) -> bool:
        try:
            conn = mysql.connector.connect(
                host=settings.MYSQL_HOST,
                port=settings.MYSQL_PORT,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                database=settings.MYSQL_DATABASE
            )
            conn.close()
            return True
        except Exception:
            return False

db_manager = DatabaseManager()