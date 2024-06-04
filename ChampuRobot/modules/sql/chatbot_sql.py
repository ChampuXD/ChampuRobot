import threading

from sqlalchemy import Column, String

from ChampuRobot.modules.sql import BASE, SESSION


class ChampuChats(BASE):
    __tablename__ = "Champu_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


ChampuChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_Champu(chat_id):
    try:
        chat = SESSION.query(ChampuChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_Champu(chat_id):
    with INSERTION_LOCK:
        Champuchat = SESSION.query(ChampuChats).get(str(chat_id))
        if not Champuchat:
            Champuchat = ChampuChats(str(chat_id))
        SESSION.add(Champuchat)
        SESSION.commit()


def rem_Champu(chat_id):
    with INSERTION_LOCK:
        Champuchat = SESSION.query(ChampuChats).get(str(chat_id))
        if Champuchat:
            SESSION.delete(Champuchat)
        SESSION.commit()
