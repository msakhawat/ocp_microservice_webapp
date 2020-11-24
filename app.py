import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
from datetime import datetime
from kafka import KafkaProducer

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://sa:1234@mariadb/blog'
# there must be better way. see how to change port
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DATABASE_USER', 'sa')}:{os.getenv('DATABASE_PASSWORD', '1234')}@{os.getenv('DATABASE_INSTANCE_NAME', 'mysql')}/{os.getenv('DATABASE_NAME','blog')}"
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET'])
def get_posts():
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('posts.html', posts=all_posts)

@app.route('/posts/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        post = BlogPost()
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        post.date_posted= datetime.utcnow().strftime("%Y%m%d")    
        db.session.add(post)
        db.session.commit()
        ####
        
        producer = KafkaProducer(client_id='blog_post', bootstrap_servers='kafkaserver1:9092')
        
        producer.send('blog-post', str(post.id).encode())
        ####
        return redirect('/posts')
    else:
        return render_template('add.html') 

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

if __name__ == "__main__":
    app.run(debug=True)