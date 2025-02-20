# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# MySQL Database Connection
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Check if environment variables are loaded correctly
if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
    raise RuntimeError("Database environment variables not set properly!")

# Database connection function
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except Exception as e:
        raise RuntimeError(f"Failed to connect to database: {str(e)}")

# User model for registration
class User(BaseModel):
    username: str
    password: str

# Home route
@app.get("/")
def home():
    return {"message": "Algo Trading Platform API is running!"}

# User registration route
@app.post("/register")
def register(user: User):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user.username, user.password))
        db.commit()
        return {"message": "User registered successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        db.close()
