from fastapi import FastAPI, HTTPException
import sqlite3
from model import PostCreate, Post

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the CRUD API"}

def create_connection():
    connection = sqlite3.connect("posts.db")
    return connection

def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS posts (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   user TEXT NOT NULL)      
                   """)
    connection.commit()
    connection.close()

create_table()

def create_post(post: PostCreate):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO posts (title, user) VALUES (?, ?)",
                   (post.title, post.user))
    
    connection.commit()
    post_id = cursor.lastrowid
    connection.close()
    return post_id

def list_table_query():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts")
    results = cursor.fetchall()
    connection.commit()
    connection.close()
    return results


@app.post("/posts/")
def create_post_endpoint(post: PostCreate):
    post_id = create_post(post)
    return {"id": post_id, **post.dict()}


# get all posts
@app.get('/list-posts/')
def list_table_endpoint():
    result = list_table_query()
    return result

# delete posts
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    connection.commit()
    connection.close()
    return {"message": "Post deleted"}



# read post
def read_post(post_id: Post):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts where id = ?", (post_id.id,))
    post = cursor.fetchone()
    connection.close()
    return post

@app.get('/posts/{post_id}', response_model=Post)
def read_post_ep(post_id: int):
    post = read_post(Post(id=post_id))  # Call the read_post function.

    return post


# updating posts
@app.put("/posts/{post_id}", response_model=Post)
def update_post(post_id: int, post: PostCreate):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE posts SET title = ?, user = ? WHERE id = ?", (post.title, post.user, post_id))
    connection.commit()
    connection.close()
    updated_post = read_post(Post(id=post_id))  # Read the updated post from the database.
  
    return updated_post


