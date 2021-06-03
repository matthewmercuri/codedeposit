import base64
from flask_pymongo import PyMongo
from pathlib import Path

# Change to find or 404
class MongoDB:

    def __init__(self, mongo_obj):
        self.mongo = mongo_obj

    def insert_post(self, post):
        pass

    def get_post_by_id(self, id):
        return self.mongo.db.posts.find_one_or_404({"_id": id})

    def return_headline(self, id):
        pass

    def most_recent_post(self):
        return self.mongo.db.posts.find_one_or_404({"_id": self.get_last_id()})

    def recent_posts(self):
        last_id = self.get_last_id()
        recent_posts = self.mongo.db.posts.find({"_id": {"$lt": last_id}}).sort("_id", -1).limit(3)
        return recent_posts

    def get_posts(self):
        posts = self.mongo.db.posts.find().sort("_id", -1)
        return posts

    def get_db_size(self):
        num_docs = self.mongo.db.posts.count_documents()
        return num_docs

    def get_last_id(self):
        _last = self.mongo.db.posts.find().sort("_id", -1).limit(1)
        for x in _last:
            _last = x['_id']
        return _last

    def image_fixer(self, feature_base64):
        # Have to test this a lot harder
        prefix = "data:image/png;base64,"
        feature_base64 = str(feature_base64)
        result = prefix + feature_base64[2:]
        result = result[:len(result)-1]
        return result

    def test(self):
        return self.mongo.db.posts.find_one()

    def insert_test_post(self, id_num):
        _id = id_num
        _post = open(Path("numbled/test_post/testpost.txt"), "r")
        post_text = _post.read()
        title = f"This is a Title Headline and it is Very Long, Maybe Not {_id}"
        author = "Test Author"
        description = "..."
        date = "2020-08-10"
        with open(Path("numbled/test_post/feature.jpg"), "rb") as image_file:
            feature_img = base64.b64encode(image_file.read())
            feature_img = self.image_fixer(feature_img)
        post_insert = {"_id": _id, "title": title, "description": description, "author": author,
                       "date": date, "post": post_text, "featureImg": feature_img}
        self.mongo.db.posts.insert_one(post_insert)

    def return_test_post(self, id_num):
        return self.mongo.db.posts.find_one({"_id": 30})
