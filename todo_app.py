from flask import Flask, request, jsonify, render_template
from flask_table import Table, Col
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True)
    content = db.Column(db.String(100))

    def __init__(self, title, content):
        self.title = title
        self.content = content


class todoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content')

class ItemTable(Table):
    title=Col("Task")
    content = Col('Details')

todo_schema = todoSchema(strict=True)
list_schema = todoSchema(many=True, strict=True)

@app.route("/")
def table():
    todo_list = Note.query.all()
    table = ItemTable(todo_list)

    return render_template('simpleFront.html', table=table)


@app.route("/add", methods=['POST'])
def add_note():
    title = request.json['title']
    content = request.json['content']
    new_note = Note(title, content)

    db.session.add(new_note)
    db.session.commit()

    return f'<h1>item created, id: {new_note.id}</h1>'


@app.route("/delete", methods=['POST'])
def delete():
    id = request.json['id']
    deleted = []
    for i in id:
        try:
            item = Note.query.get(i)
            db.session.delete(item)

            deleted.append(i)

        except:
            pass

    db.session.commit()
    return f'<h1>Successfully deleted ids: {deleted}</h1>'

@app.route("/list", methods=['GET'])
def get_list():
    todo_list = Note.query.all()
    result = list_schema.dump(todo_list)

    return jsonify(result.data)

if(__name__ == "__main__"):
    app.run(debug=True)
