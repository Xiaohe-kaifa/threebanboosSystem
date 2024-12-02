from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer

class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 有客户端来向后端发送websocket连接的请求时，自动触发
        # 服务器允许和客户端创建连接
        print('连接上了')
        self.accept()
        self.send("来了啊客户")#给客户端发送消息
        # 不允许创建连接
        # raise StopConsumer()
    def websocket_receive(self, message):
        # 浏览器基于websocket向后端发送数据，自动触发接受消息。
        print('结束到的消息：'+message['text'])
        self.send(message['text'])
        # 服务端主动断开连接
        # self.close()
    def websocket_disconnect(self, message):
        # 客户端与服务器断开连接时自动触发
        print('断开连接')
        raise StopConsumer()