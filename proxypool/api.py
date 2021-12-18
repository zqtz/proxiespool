from .db import RedisClient
from flask import Flask,g

# __all__ = ['app']
app = Flask(__name__)

def get_conn():
    # 如果当前没有redis连接则新建一个连接
    if not hasattr(g,'redis_client'):
        g.redis_client = RedisClient()
    return g.redis_client

@app.route('/')
def index():
    return 'welcome to the proxies system'


@app.route('/get')
def get():
    #获取一个代理
    conn = get_conn()
    return conn.pop()

@app.route('/count')
def get_counts():
    # 获取代理的个数
    conn = get_conn()
    return str(conn.queue_len)




if __name__ == '__main__':
    app.run()