import os
import pymysql
from fastapi import FastAPI, Path
from dotenv import load_dotenv

# load_dotenv(dotenv_path=r"E:\PythonProjects\unikraft_challenge\.env")
#load_dotenv(dotenv_path="./.env")  # Adjust the path as necessary

app = FastAPI()

# def get_connection():
#     return pymysql.connect(
#         host=os.getenv("DB_HOST"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         db=os.getenv("DB_NAME"),
#         cursorclass=pymysql.cursors.DictCursor
#     )

def get_connection():
    return pymysql.connect(
        host="mysql",
        user="root",
        port=3306,
        password="root",
        db="movie_db",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/movies")
def get_movies():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT m.*, GROUP_CONCAT(g.name) as genres
                FROM home_movie m
                LEFT JOIN home_movie_genre mg ON m.id = mg.movie_id
                LEFT JOIN home_genre g ON g.id = mg.genre_id
                GROUP BY m.id
                LIMIT 50
            """)
            result = cursor.fetchall()
        return result
    finally:
        conn.close()

@app.get("/genres")
def get_genres():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM home_genre")
            return cursor.fetchall()
    finally:
        conn.close()

@app.get("/movies/{movie_id}")
def get_movie_by_id(movie_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT m.*, GROUP_CONCAT(g.name) as genres
                FROM home_movie m
                LEFT JOIN home_movie_genre mg ON m.id = mg.movie_id
                LEFT JOIN home_genre g ON g.id = mg.genre_id
                WHERE m.id = %s
                GROUP BY m.id
            """, (movie_id,))
            return cursor.fetchone()
    finally:
        conn.close()
