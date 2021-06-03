from flask import Flask
from flask import render_template
from flask_pymongo import PyMongo
from db import MongoDB

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://site:site123@cluster0-c2zy3.mongodb.net/numbledlive?retryWrites=true&w=majority"
mongo = PyMongo(app)
mongodb = MongoDB(mongo)


@app.route('/home')
@app.route('/')
def home():
    feature = mongodb.most_recent_post()
    recent_posts = mongodb.recent_posts()
    return render_template('index.html', page_title='home', feature=feature,
                           recent_posts=recent_posts)


@app.route('/blog')
def blog():
    posts = mongodb.get_posts()
    return render_template('blog.html', posts=posts, page_title='Blog')


@app.route('/about')
def about():
    return render_template('about.html', page_title='About')


@app.route('/blog/<int:postid>')
def post_page(postid):
    post = mongodb.get_post_by_id(postid)
    return render_template('post.html', post=post, page_title=post['title'])

# @app.route('/dbtest')
# def db():
#     test = mongodb.test()
#     mongodb.insert_test_post(30)
#     return str(test)

# @app.route('/debug')
# def debug():
#     _result = mongodb.get_last_id()
#     return _result

# def url_encode(url):
#     return urllib.parse.quote(url)

# def url_decode(url):
#     return urllib.parse.unquote(url)


if __name__ == '__main__':
    app.run(debug=True)
