
import os
import mysql.connector

from contextlib import contextmanager
from mysql.connector import pooling

class Database:
    _pool = None
        
    @classmethod
    def _get_pool(cls):
        if cls._pool is None:
            cls._pool = pooling.MySQLConnectionPool(
                pool_name="app_pool",
                pool_size=5,
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                autocommit=False,
            )
        return cls._pool

    @classmethod
    @contextmanager
    def get_connection(cls):
        conn = cls._get_pool().get_connection()
        
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
            
    @classmethod
    def check(cls):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
        try:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        finally:
            cursor.close()
            
    