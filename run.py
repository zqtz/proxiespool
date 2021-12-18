from proxypool.api import app
from proxypool.schedule import Schedule


# 启动调度器和api
def main():
    s = Schedule()
    s.run()
    app.run()




if __name__ == '__main__':
    main()