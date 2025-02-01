import requests
import json 
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# Endpoint to retrieve posts from an external API. Accepts an optional postId query parameter.
@app.get("/posts/")
def get_posts(postId: Optional[int] = None):
    if postId is None:
        posts = requests.get('https://jsonplaceholder.typicode.com/posts')
        response = json.loads(posts.text)
    else:
        posts = requests.get(f'https://jsonplaceholder.typicode.com/posts/{postId}')
        response = json.loads(posts.text)
    
    return response

# Endpoint to retrieve comments from an external API. Accepts an optional postId query parameter.
@app.get("/comments/")
def get_comments(postId: Optional[int] = None):
    if postId is None:
        comments = requests.get('https://jsonplaceholder.typicode.com/comments')
        response = json.loads(comments.text)
    else:
        comments = requests.get(f'https://jsonplaceholder.typicode.com/comments/?postId={postId}')
        response = json.loads(comments.text)
    
    return response

# Endpoint to get posts by a specific user, filtered and formatted by userID
@app.get("/formatted_posts/{userID}")
def get_post_then_format_according_to_user(userID: int):
    posts = get_posts()  # Retrieve posts from get_posts function
    data = {"userID": userID, "posts": []}
    for post in posts:
        if post['userId'] == userID:
            data["posts"].append({
                "post_title": post["title"],
                "post_body": post["body"],
            })
    return data

# Endpoint to get comments by post ID, filtered and formatted based on postID
@app.get("/formatted_comment/{postID}")
def get_post_then_format_according_to_user(postID: int):
    req = requests.get(f'http://127.0.0.1:8000/comments/?postId={postID}')
    comments = json.loads(req.text)
    data = {"post_id": postID, "comments": []}
    for comment in comments:
        if comment['postId'] == postID:
            data["comments"].append({
                "commenter_email": comment["email"],
                "commenter_name": comment["name"],
                "comment": comment["body"],
            })
    return data

# New endpoint: /detailed_post/{userID}
# Retrieves posts by userID and includes comments for each post
@app.get("/detailed_post/{userID}")
def get_detailed_post(userID: int):
    posts = get_posts()  # Fetch all posts
    data = {"userID": userID, "detailed_posts": []}
    
    for post in posts:
        if post["userId"] == userID:
            # Retrieve comments for each post using postId
            post_comments = requests.get(f'http://127.0.0.1:8000/comments/?postId={post["id"]}')
            comments = json.loads(post_comments.text)
            post_data = {
                "post_title": post["title"],
                "post_body": post["body"],
                "comments": [{"commenter_email": c["email"], "commenter_name": c["name"], "comment": c["body"]} for c in comments]
            }
            data["detailed_posts"].append(post_data)
    
    return data
