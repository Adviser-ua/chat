# coding=UTF-8
# script create by Konstantyn Davidenko
# mail: kostya_ya@it-transit.com

from database import Connection
from flask import render_template, redirect, session, url_for, request


conn = Connection()
class PrivateMess:

    def __init__(self, username, mess):
        from sqlalchemy import func
        self.time = func.now()
        self.author = username
        self.message = mess

def home():
    kw = {}
    if session.get('logged_in'):
        user = conn.get_user_by_name(session.get('username'))
        kw['mychats'] = conn.get_my_chats(user.id)
    kw['chats'] = conn.get_chats()
    kw['username'] = session.get('username')
    kw['title'] = 'Chats'
    return render_template('index.html', **kw)

def login(user, password):
    user = conn.check_credention(login=user, password=password)
    if user:
        session['username'] = user.name
        session['logged_in'] = True
    return redirect(url_for('index'))

def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('logged_in', None)
    return redirect(url_for('index'))


def confirm_register(username, password, password_confirm, email='', phone=''):
    if username and password == password_confirm:
        try:
            conn.new_user(name=username, password=password, email=email, phone=phone)
            session['username'] = username
            login(username, password)
            return redirect(url_for('index'))
        except Exception, e:
            return redirect(url_for('register'))
    else:
        return redirect(url_for('register'))


def register(error=None):
    if error:
        return render_template('register.html', **error)
    else:
        return render_template('register.html')

def chat(chat_id, messages=None):
    kw = {}
    kw['chat'] = conn.get_chat(chat_id)
    kw['owner'] = conn.get_user_by_id(kw['chat'].owner)
    kw['messages'] = conn.get_messages(chat_id)
    if session.get('logged_in'):
        user = conn.get_user_by_name(session.get('username'))
        kw['mychats'] = conn.get_my_chats(user.id)
    kw['username'] = session.get('username')
    if messages:
        kw['messages'].extend(messages)
    return render_template('chat.html', **kw)

def addchat(chat_id):
    user = conn.get_user_by_name(session['username'])
    conn.add_user_to_chat(user_id=user.id, chat_id=chat_id)
    return redirect(url_for('chat', chat_id=chat_id))

def new_chat(name):
    username = session.get('username')
    user_id = conn.get_user_by_name(username).id
    chat_id = conn.new_chat(name=name, user_id=user_id)
    return redirect(url_for('enter_to_chat', chat_id=chat_id))

def runcomand(chat_id, message):
    if '/sum' in message:
        vals = [float(x.strip()) for x in message.split(',') if x.isdigit()]
        new_mess = [PrivateMess(session.get('username'), sum(vals))]
    else:
        new_mess = [PrivateMess(session.get('username'), 'test')]
    return chat(chat_id, new_mess)


def messageToChat(chat_id, message, username):
    if session.get('logged_in'):
        username = session.get('username')
    else:
        session['username'] = username
    conn.new_message(user_id=username, chat_id=chat_id, message=message)
    return redirect(url_for('chat', chat_id=chat_id))

def find_chat(query):
    kw = {}
    if session.get('logged_in'):
        user = conn.get_user_by_name(session['username'])
        kw['mychats'] = conn.get_my_chats(user.id)
    kw['chats'] = conn.find_chat(query)
    kw['username'] = session.get('username')
    kw['title'] = 'Found Chats'
    return render_template('index.html', **kw)

def clear():
    session['username'] = ''
    session['logged_in'] = ''
    return redirect(url_for('index'))

def get_history(chat_id):
    kw = {'messages': conn.get_messages(chat_id)}
    return render_template('chat_history.html', **kw)

def get_members(chat_id):
    kw = {'members': conn.get_users(chat_id)}
    return render_template('members.html', **kw)

def delete_from_my_chats(chat_id):
    print request.authorization
    username = session.get('username')
    user_id = conn.get_user_by_name(username).id
    conn.delete_from_my_chats(user_id, chat_id)
    return redirect('/')
