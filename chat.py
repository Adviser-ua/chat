# coding=UTF-8
# script create by Konstantyn Davidenko
# mail: kostya_ya@it-transit.com
#

"""
Основной файл приложения
"""

import view
from flask import request
from flask import Flask
from datetime import timedelta

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.secret_key = 'kostya the best developer!'
app.config['SESSION_TYPE'] = 'filesystem'
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        return view.login(login, password)
    else:
        return view.home()


@app.route('/register', methods=['GET', 'POST'])
def register(error=None):
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')
        password_confirm = request.form.get('passwordConfirm')
        email = request.form.get('mail')
        phone = request.form.get('phone')
        return view.confirm_register(username=username, password=password, password_confirm=password_confirm, email=email, phone=phone)
    else:
        return view.register(error)

@app.route('/logout/')
def logout():
    return view.logout()

@app.route('/chat/<chat_id>/')
def enter_to_chat(chat_id):
    return view.chat(chat_id)


@app.route('/chat/<chat_id>/')
def chat(chat_id):
    return view.chat(chat_id)

@app.route('/clear')
def clear():
    return view.clear()

@app.route('/new_chat/', methods=['POST'])
def new_chat():
    subject = request.form['subject']
    return view.new_chat(subject)

@app.route('/find_chat/', methods=['POST'])
def find_chat():
    query = request.form['query']
    return view.find_chat(query)

@app.route('/addchat/<chat_id>')
def addchat(chat_id):
    return view.addchat(chat_id)

@app.route('/delete_from_my_chats/<chat_id>')
def delete_from_my_chats(chat_id):
    return view.delete_from_my_chats(chat_id)

@app.route('/send_mess/', methods=['POST'])
def send_mess():
    chat_id = request.form.get('chat_id')
    author = request.form.get('username')
    message = request.form.get('message')
    return view.messageToChat(chat_id=chat_id, message=message, username=author)

@app.route("/get_history/<chat_id>", methods=['GET', 'POST'])
def get_history(chat_id):
    return view.get_history(chat_id)


@app.route("/get_members/<chat_id>", methods=['POST'])
def get_members(chat_id):
    return view.get_members(chat_id)

if __name__ == '__main__':
    app.run()