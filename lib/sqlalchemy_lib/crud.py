from sqlalchemy.orm import Session
from .model import ServerInfo
from time import struct_time as t

def add_user_info(db: Session,user_id:int, channel_id:int, user_balance:int):

    userinfo = ServerInfo(user_id=user_id,
                          channel_id=channel_id,
                          user_balance=user_balance)
    db.add(userinfo)
    db.commit()

def add_channel(db: Session, channel_id: int):
    exists = db.query(ServerInfo).filter_by(channel_id=channel_id).first()
    if exists:
        return False

    obj = ServerInfo(channel_id=channel_id)
    db.add(obj)
    db.commit()
    return True


def remove_channel(db: Session, channel_id: int):
    row = db.query(ServerInfo).filter_by(channel_id=channel_id).first()
    if not row:
        return False

    db.delete(row)
    db.commit()
    return True


def is_initialized(db: Session, channel_id: int) -> bool:
    return db.query(ServerInfo).filter_by(channel_id=channel_id).first() is not None
