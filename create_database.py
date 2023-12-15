from flask_blog.models import User, Post
from flask_blog import database, app

database.drop_all()
database.create_all()
user_1 = User(username = 'Alice', email = 'alice@demo.com', password = 'example_1')
database.session.add(user_1)
user_2 = User(username = 'Bob', email = 'bob@demo.com', password = 'example_2')
database.session.add(user_2)

post_1 = Post(title = 'First Post', content = 'First post on this blog!', user_id = user_1.id)
database.session.commit()
