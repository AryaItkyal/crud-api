from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List
from schema import Post
from random import randrange
import sqlite3

app = FastAPI()


## crud using sql for posts only

def create_connection(database_name="tweet.db"):
    connection = sqlite3.connect(database_name)
    return connection

def initialize_database(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            published TEXT NOT NULL
        )
    """)
    cursor.close()
    connection.commit()

def get_connection_and_initialize():
    connection = create_connection()
    initialize_database(connection)
    connection.close()
    return 'database ready!'

# get_connection_and_initialize()


# my_posts = [{"title": "title of post 1", "content": "content of post 1","id":1}, 
#             {"title": "fav foods", "content": "I like pizza", "id":2}]

my_posts=[]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_post_index(id):
    for i in range(len(my_posts)):
        if my_posts[i]['id'] == id:
            return i

@app.get("/") # decorator 
async def root():
    return {"message": "welcome to my CRUD api"}

@app.get("/posts")
def get_posts():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
                    SELECT * FROM posts;
                   """)
    data = cursor.fetchall()

    connection.commit()

    cursor.close()
    connection.close()

    return {"data": data}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
                    INSERT INTO posts (title, content, published)
                   VALUES (?, ?, ?);
                   """, (post.title, post.content, post.published))
    # print(post.rating)
    last_row_id = cursor.lastrowid
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 10000000)

    # my_posts.append(post_dict)
    # print(new_post.dict())
    connection.commit()
    cursor.close()
    connection.close()

    return {"id": last_row_id, **post.dict()}

# order matters
# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[-1]
#     return {"detail": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # print(type(id))
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
                    SELECT * FROM posts where id = ?;
                   """, (id,))
    data = cursor.fetchone()
   
    connection.commit()
    cursor.close()
    connection.close()

    # post = find_post(id)
    if not data:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} not found"}
    return {"post_detail": data}


@app.delete("/posts/{id}")
def del_post(id: int, response: Response):
    # ind = find_post_index(id)
    connection = create_connection()
    cursor = connection.cursor()

    # before = cursor.rowcount

    cursor.execute("""
                    DELETE FROM posts where id = ?;
                   """, (id,))
    # data = cursor.fetchone()
   
    altered_rows = cursor.rowcount

    connection.commit()
    cursor.close()
    connection.close()

    if altered_rows < 1:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
        

    return {'message': 'post was successfully deleted!'}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
                    UPDATE posts SET title=?, content=?, published=?
                   WHERE id = ?;
                   """, (post.title,post.content,post.published, id))
    # data = cursor.fetchone()
    altered_rows = cursor.rowcount
   
    connection.commit()
    cursor.close()
    connection.close()

    # ind = find_post_index(id)
    if altered_rows < 1:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
        
    # post_dict = post.dict()
    # post_dict['id'] = id

    # my_posts[ind] = post_dict


    # print(post)

    return {"message": 'Post updated!'}