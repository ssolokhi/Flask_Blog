from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [
    {
        'author': 'Bob',
        'title': 'Blog Post 1',
        'content': 'First post',
        'data': 'April 1, 2023'
    },
    {
        'author': 'Alice',
        'title': 'Blog Post 2',
        'content': 'Second post',
        'date': 'April 1, 2023'
    }
]

@app.route("/") # create home page
@app.route("/home") # alias
def home():
    return render_template('home.html', posts = posts)

@app.route("/about") # create home page
def about():
    return render_template('about.html', title = 'About')

if __name__ == '__main__':
    app.run(debug = True)