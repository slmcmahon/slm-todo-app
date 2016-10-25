from flask import Flask, render_template, redirect, request
from google.appengine.api import users
from todomanager import TodoManager
import time
from datetime import datetime, timedelta

app = Flask(__name__)
DEBUG = True


@app.route('/')
def get_todo_items():
    user = users.get_current_user()
    if not user:
        return redirect(users.create_login_url('/'))

    show_closed = False if not request.args.get('closed') == 'true' else True

    # set the due date to 1 day in the future by default
    duedate = datetime.today() + timedelta(days=1)
    values = {
        'now': str(duedate)[:16],
        'closed': show_closed,
        'todos': TodoManager.get_todo_items(user, show_closed)
    }

    return render_template('todolist.html', data=values)


@app.route('/addtodo', methods=['POST'])
def add_todo():
    user = users.get_current_user()
    if not user:
        return redirect(users.create_login_url('/addtodo'))

    text = request.form['todotext']
    due = request.form['duedate']

    due_date = None

    if due:
        due_date = datetime.strptime(due, "%Y-%m-%d %H:%M")


    TodoManager.add_todo(user, text, due=due_date)

    if DEBUG:
        time.sleep(.5)

    return redirect('/')


@app.route('/completetodo/<key>')
def complete_todo(key):
    user = users.get_current_user()
    if not user:
        return redirect(users.create_login_url('completetodo/{}'.format(key)))

    TodoManager.close_todo(key)

    if DEBUG:
        time.sleep(.5)

    return redirect('/')


@app.route('/deletetodo/<key>')
def delete_todo(key):
    user = users.get_current_user()
    if not user:
        return redirect(users.create_login_url('completetodo/{}'.format(key)))

    TodoManager.delete_todo(key)

    if DEBUG:
        time.sleep(.5)

    return redirect('/')

if __name__ == '__main__':
    app.run()
