from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = ToDo(title=title , desc=desc)
        db.session.add(todo)
        db.session.commit()
    allToDos = ToDo.query.all()
    return render_template('index.html', allToDos=allToDos) 

@app.route('/show')
def show_todos():
    allToDos = ToDo.query.all()
    print(allToDos)
    return "Todos"

@app.route('/delete/<int:id>')
def delete_todo(id):
    todo = ToDo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_todo(id):
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = ToDo.query.filter_by(id=id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = ToDo.query.filter_by(id=id).first()
    return render_template("update.html", todo=todo)

if __name__ == "__main__":
    app.run(debug=True, port=8000)