import requests
from flask import Flask, render_template, request, redirect, url_for
import json
import uuid
from datetime import datetime

app = Flask(__name__)

# Blog posts list
blog_posts = []


# Function to fetch blog posts from a JSON file
def fetch_blog_posts():
    """
    Fetch blog posts from a JSON file.
    """
    try:
        with open('data/blog_posts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
    except json.JSONDecodeError:
        return []  # Return an empty list if the JSON is invalid


# Home route to display all blog posts
@app.route('/')
def index():
    """
    Home route that displays all blog posts.
    """
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    """
    Adds a new blog post.

    If the request method is POST, extracts data from the form and adds a new
    post to the blog_posts list. Each post is assigned a unique ID using UUID.
    """
    if request.method == 'POST':
        # Get form data
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Generate a unique string-based ID for the new post
        new_post = {
            "id": str(uuid.uuid4()),  # Generate a unique ID
            "author": author,
            "title": title,
            "content": content,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        blog_posts.append(new_post)

        # Redirect to the homepage
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<post_id>', methods=['GET'])
def delete_post(post_id):
    """
    Deletes a blog post by its ID.

    Args:
        post_id (str): ID of the blog post to be deleted.

    Returns:
        Redirects to the index page after deletion.
    """
    global blog_posts
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    return redirect(url_for('index'))


@app.route('/update/<uuid:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    """
    Updates an existing blog post.
    On GET: Displays the current post details in a form.
    On POST: Updates the post details in the blog_posts list.
    """
    # Find the post by ID
    post = next((post for post in blog_posts if str(post["id"]) == str(post_id)), None)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Update post details
        post["title"] = request.form.get('title', post["title"])
        post["content"] = request.form.get('content', post["content"])
        post["author"] = request.form.get('author', post["author"])
        post["date"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Redirect back to the home page
        return redirect(url_for('index'))

    # Render the update form
    return render_template('update.html', post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
