from sqlalchemy.orm import Session
from .model import ServerInfo

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
