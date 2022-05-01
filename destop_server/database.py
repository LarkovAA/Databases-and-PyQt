import sys
sys.path.append('..')
import os
from datetime import datetime
import sqlite3 as sql3
import sqlalchemy as sal
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from common.configurable_variables import PATH_BF
try:
    from admins import PATH_BD, NAME_BD

    if PATH_BD and NAME_BD:
        PATH_BF = f'{PATH_BD}/NAME_BD'
except:
    pass
engin = sal.create_engine(f'sqlite:///{PATH_BF}', echo=False, pool_recycle=7200,connect_args={'check_same_thread': False})

Base = declarative_base()

class Client(Base):
    __tablename__ = 'client'
    id = sal.Column(sal.Integer, primary_key=True)
    login = sal.Column(sal.String, unique=True)
    password = sal.Column(sal.String)
    info = sal.Column(sal.String, nullable=True)

    def __init__(self, login, info):
        self.login = login
        self.info = info

    def __repr__(self):
        return f'{self.id}, {self.login}, {self.info}'

class HistoryClient(Base):
    __tablename__ = 'history_client'
    id = sal.Column(sal.Integer, primary_key=True)
    id_client = sal.Column(sal.Integer, sal.ForeignKey('client.id'), unique=True)
    entry_time = sal.Column(sal.DateTime, )
    ip_adress = sal.Column(sal.Integer)

    def __init__(self, id_client, entry_time, ip_adress):
        self.id_client = id_client
        self.entry_time = entry_time
        self.ip_adress = ip_adress

    def __repr__(self):
        return f'{self.id}, {self.id_client}, {self.entry_time},{self.ip_adress}'

class ListContact(Base):
    __tablename__ = 'list_contact'
    id = sal.Column(sal.Integer, primary_key=True)
    id_owner = sal.Column(sal.Integer, sal.ForeignKey('client.id'))
    id_client = sal.Column(sal.Integer, sal.ForeignKey('client.id'))

    def __init__(self, id_owner, id_client):
        self.id_owner = id_owner
        if id_owner != id_client:
            self.id_client = id_client
        else:
            raise ValueError('Вы не можете добавить в друзья самого себя')

    def __repr__(self):
        return f'{self.id}, {self.id_owner}, {self.id_client}'

metadata = Base.metadata
metadata.create_all(engin)

Session = sessionmaker(bind=engin)
sess = Session()

if __name__ == "__main__":
    # Пример добавления новых элементов в таблицу Client
    # try:
    #     client1 = Client('client1', 'клиент 1')
    #     sess.add(client1)
    #     client2 = Client('client2', 'клиент 2')
    #     sess.add(client2)
    #     sess.commit()
    # except:
    #     pass
    #
    # result = sess.query(Client).filter_by(login='client1').first()
    # print('rows count: ', result)

    # Пример добавления новых элементов в таблицу HistoryClient она уже встроена в работу сервера
    # result = sess.query(Client).filter_by(login='client1').first()
    # customer_verification = sess.query(HistoryClient).filter_by(id_client=result.id).first()
    # if customer_verification:
    #     customer_verification.entry_time = datetime.now()
    #     sess.commit()
    # else:
    #     new_time = HistoryClient(result.id, datetime.now(), '192.170.3.11')
    #     sess.add(new_time)
    #     sess.commit()

    # Пример добавления новых элементов в таблицу ListContact

    # list_contact_1 = ListContact(1, 2)
    # list_contact_2 = ListContact(2, 1)
    # sess.add(list_contact_1)
    # sess.add(list_contact_2)
    # sess.commit()

    # Поиск слиска контактов
    # id_user = sess.query(Client).filter_by(login='client1').first()
    # id_user = str(id_user).split(', ')[0]
    # list_contact = sess.query(ListContact).filter_by(id_owner=id_user).all()
    # text = 'Ваш список контактов: '
    # for id in list_contact:
    #     id = id.id_client
    #     name_contact = sess.query(Client).filter_by(id=id).first()
    #     name_contact = str(name_contact).split(', ')[1]
    #     text += f' {name_contact}'
    # print(text)

    # Удаление из контактов
    # id_del_user = sess.query(Client).filter_by(login='client2').first()
    # if id_del_user:
    #     id_user = sess.query(Client).filter_by(login='client1').first()
    #     id_user = id_user.id
    #     id_del_user = id_del_user.id
    #     # del_contact = sess.query(ListContact).filter_by(id_owner=id_user, id_client=id_del_user).first()
    #     print(del_contact)
    #     # del_contact.delete()
    #     # sess.commit()
    # else:
    #     print('Ошибка')

    # Добавление
    # id_add_user = sess.query(Client).filter_by(login='client2').first()
    # if id_add_user:
    #     id_user = sess.query(Client).filter_by(login='client1').first()
    #     id_user = str(id_user).split(', ')[0]
    #     id_add_user = str(id_add_user).split(', ')[0]
    #     new_contact = ListContact(id_user, id_add_user)
    #     sess.add(new_contact)
    #     sess.commit()
    # else:
    #     print('Ошибка')
    pass