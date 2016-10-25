from flask import Flask, render_template, redirect, request
from google.appengine.api import users
from todomanager import TodoManager

app = Flask(__name__)


@app.route('/')
def get_todo_items():
    user = users.get_current_user()
    if not user:
        return redirect(users.create_login_url('/'))

    mgr = TodoManager()
    todos = mgr.get_todo_items(user)

    return render_template('todolist.html', data={'todos': todos})


@app.route('/addtodo', methods=['POST'])
def add_todo():
    user = users.get_current_user()
    if not user:
        return redirect(users.create_login_url('/addtodo'))

    text = request.form["todotext"]
    TodoManager.add_todo(user, text)
    return redirect('/')


@app.route('/completetodo/<key>')
def complete_todo(key):
    user = users.get_current_user()
    if not user:
        return redirect(users.create_login_url('completetodo/{}'.format(key)))

    TodoManager.close_todo(key)
    return redirect('/')


@app.route('/deletetodo/<key>')
def delete_todo(key):
    user = users.get_current_user()
    if not user:
        return redirect(users.create_login_url('completetodo/{}'.format(key)))

    TodoManager.delete_todo(key)
    return redirect('/')

if __name__ == '__main__':
    app.run()
