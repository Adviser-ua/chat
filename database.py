# coding=UTF-8
# script create by Konstantyn Davidenko
# mail: kostya_ya@it-transit.com
#

"""
Модель БД и управляющий класс
"""


from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import json
import os


Base = declarative_base()

class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner = Column(String)

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    chat = Column(String)
    message = Column(String)
    author = Column(String)
    time = Column(DateTime, default=func.now())

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    hired_on = Column(DateTime, default=func.now())
    password = Column(String)
    email = Column(String)
    phone = Column(String)

    def json(self):
        return json.dumps({'username': self.name,
                          'email': self.email,
                          'phone': self.phone},)

class Relation(Base):
    __tablename__ = 'relation'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    user_id = Column(Integer)

class Connection:

    def __init__(self):
        from sqlalchemy import create_engine
        # self.engine = create_engine('sqlite:///chats.db')
        db_login = 'adminsqinfjv'
        db_pass = 'NCMaeAr3ghPN'
        db_host = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
        db_port = os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']
        db_name = 'chat'
        self.engine = create_engine('postgresql://{db_login}:{db_pass}@{db_host}:{db_port}/{db_name}'.format(db_login=db_login, db_pass=db_pass, db_host=db_host, db_port=db_port, db_name=db_name))
        from sqlalchemy.orm import sessionmaker
        session = sessionmaker()
        session.configure(bind=self.engine)
        self.session = session()
        self.create_table()

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def new_chat(self, name, user_id):
        chat = Chat(name=name, owner=user_id)
        self.session.add(chat)
        self.session.commit()
        return chat.id

    def get_chats(self):
        return self.session.query(Chat).all()


    def get_chat(self, chat_id):
        return self.session.query(Chat).filter_by(id=chat_id).one()

    def new_user(self, name, password, email='', phone=''):
        user = User(name=name, password=password, email=email, phone=phone)
        self.session.add(user)
        self.session.commit()

    def add_user_to_chat(self, user_id, chat_id):
        relation = Relation(user_id=user_id, chat_id=chat_id)
        self.session.add(relation)
        self.session.commit()

    def get_user_by_name(self, name):
        return self.session.query(User).filter_by(name=name).one()

    def get_user_by_id(self, user_id):
        return self.session.query(User).filter_by(id=user_id).one()

    def users_in_chat(self, chat_id):
        return self.session.query(Relation).filter_by(chat_id=chat_id).all()

    def new_message(self, user_id, chat_id, message):
        if user_id == '':
            user_id = 'Guest'
        mess = Message(author=user_id, chat=chat_id, message=message)
        self.session.add(mess)
        self.session.commit()

    def get_messages(self, chat_id):
        return self.session.query(Message).filter_by(chat=chat_id).all()

    def get_my_chats(self, user_id):
        sq = [x.chat_id for x in self.session.query(Relation).filter_by(user_id=user_id)]
        q = self.session.query(Chat).filter(Chat.id.in_(sq)).all()
        return q

    def get_users(self, chat_id):
        sq = [x.user_id for x in self.session.query(Relation).filter_by(chat_id=chat_id)]
        q = self.session.query(User).filter(User.id.in_(sq)).all()
        return q

    def check_credention(self, login, password):
        try:
            rs = self.session.query(User).filter_by(name=login).one()
            if rs.password == password:
                return rs
        except:
            return None

    def delete_from_my_chats(self, user_id, chat_id):
        sq = self.session.query(Relation).filter_by(user_id=user_id, chat_id=chat_id).one()
        self.session.delete(sq)
        return sq

    def find_chat(self, query):
        rs = []
        index = 0
        for i in self.session.query(Chat.name.like("%"+query+"%")).all():
            if i[0]:
                rs.append(self.session.query(Chat).all()[index])
            index += 1

        return rs