from datetime import datetime
from . import db


class User(db.Model):
    """
    用户资料表
    """
    __tablename__ = 'tb_user'

    id = db.Column(db.Integer, primary_key=True, doc='用户ID')
    name = db.Column('username', db.String, doc='昵称')
    avatarUrl = db.Column(db.String, doc='头像')
    gender = db.Column(db.Integer, default=0, doc='性别')
    password = db.Column(db.String(128), doc='密码')
    mobile = db.Column('phone', db.String, doc='手机号')
    ctime = db.Column('createTime', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('updateTime', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    email = db.Column(db.String, doc='邮箱')
    status = db.Column('isValid', db.Integer, default=1, doc='状态，是否可用')
