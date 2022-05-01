import sys
sys.path.append('..')
import sqlalchemy as sal
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from database import ListContact, Client,sess as sess_server
from destop_server.database import Client, HistoryClient, ListContact, sess as sess_server

class ClientDatabase():

    Base = declarative_base()

    class ListContact(Base):

        __tablename__ = 'list_contact'
        id = sal.Column(sal.Integer, primary_key=True)
        name_contact_client = sal.Column(sal.String)

        def __init__(self, name_contact_client):
            self.name_contact_client = name_contact_client

        def __repr__(self):
            return f'{self.id}, {self.name_contact_client}'

    class HistoryMessege(Base):

        __tablename__ = 'history_messege'
        id = sal.Column(sal.Integer, primary_key=True)
        who_sent_it = sal.Column(sal.String)
        sent_to_whom = sal.Column(sal.String)
        text = sal.Column(sal.String)

        def __init__(self, who_sent_it, sent_to_whom, sent_whom):

            self.who_sent_it = who_sent_it
            self.sent_to_whom = sent_to_whom
            self.sent_whom = sent_whom

        def __repr__(self):
            return f'{self.id}, {self.who_sent_it}, {self.sent_to_whom}, {self.sent_whom}'

    def __init__(self, dir, name):
        self.path_client_database = f'{dir}/database_client{name}.db'
        pcd = self.path_client_database
        self.engin = sal.create_engine(f'sqlite:///{pcd}', echo=False,pool_recycle=7200,connect_args={'check_same_thread': False})
        self.Base.metadata.create_all(self.engin)

        Session = sessionmaker(bind=self.engin)
        self.sess = Session()

        list_contact = self.sess.query(self.ListContact).all()
        if list_contact:
            self.sess.query(self.ListContact).delete()
            self.sess.commit()


    # вывести список контактов
    def print_list_contact(self):
        list_contact = self.sess.query(self.ListContact).all()
        return list_contact

    # записать в БД клиента данные по контактам из БД Сервера
    def record_databaise_list_contact(self, name):
        list_contact = self.sess.query(self.ListContact).all()
        if list_contact:
            self.sess.query(self.ListContact).delete()
            self.sess.commit()

        id_user = sess_server.query(Client).filter_by(login=name).first()
        list_contact = sess_server.query(ListContact).filter_by(id_owner=id_user.id).all()
        for el in list_contact:
            name_contact_client = sess_server.query(Client).filter_by(id=el.id_client).first()
            name_contact_client = name_contact_client.login
            user = self.ListContact(name_contact_client)
            self.sess.add(user)
            self.sess.commit()

    def add_contact(self, new_contact):
        new_user = ListContact(str(new_contact))
        self.sess.add(new_user)
        self.sess.commit()

    def del_contact(self, del_contact):
        cont = self.sess.query(ListContact).filter_by(name_contact_client=del_contact).first()
        cont.delete()

    def add_history_messege(self, who, whom, text):
        messege = self.HistoryMessege(who, whom, text)
        self.sess.add(messege)
        self.sess.commit()

    def list_history_messege(self, user):
        print(user)
        list_history = self.sess.query(self.HistoryMessege).filter(sal.or_(who_sent_it=user, sent_to_whom=user)).all()
        return_list_history = []
        for history in list_history:
            return_list_history.append([history.id, history.who_sent_it, history.sent_to_whom, history.text])
        return return_list_history
        # query = self.session.query(self.MessageHistory).filter_by(contact=contact)
        # return [(history_row.contact, history_row.direction,
        #          history_row.message, history_row.date)
        #         for history_row in query.all()]

if __name__ == "__main__":
    pass