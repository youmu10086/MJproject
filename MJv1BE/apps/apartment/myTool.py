import hashlib
import random
import uuid
from datetime import datetime


def get_random_str():
    # 获取随机数
    uuid_val = uuid.uuid4()
    # 转字符串
    uuid_str = str(uuid_val).encode('utf-8')
    # 获取md5实例
    md5 = hashlib.md5()
    # 拿摘要
    md5.update(uuid_str)
    # 返回
    return md5.hexdigest()


def get_cno():
    # 获取当前时间
    now = datetime.now()
    return f"{now.year}{now.month}{now.day}{now.hour}{now.minute}{random.randint(1000, 9999)}"
