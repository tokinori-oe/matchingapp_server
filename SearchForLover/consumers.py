import json
from channels.generics.websocket import AsyncWebsocketConsumer
from .models import RequestForLoverModel

class RequestConsumer(AsyncWebsocketConsumer):
    async def connect(self): #asyncは非同期コードを定義するために使用される
        await self.accept() #awaitはasyncとともに用いられるもので、asyncの中で非同期操作を行う部分にはawaitを使用する
        
    async def disconnect(self, close_code):
        pass
    
    async def receive(self, text_data):
        #メッセージを受信し、DBに保存
        data = json.loads(text_data) #json.loadsでデシリアライズ
        sender = data['sender']
        receiver = data['receiver']
       
        # バリデーションの追加
        if not sender or not receiver:
            # 必要なデータが欠落している場合はエラーメッセージを送信して処理を中断
            await self.send(text_data=json.dumps({'error': 'Incomplete data received'}))
            return
       
        #statusはデフォルトでpendingになってるけどそこはどうなるん？
        message = RequestForLoverModel(sender=sender, receiver=receiver)
        message.save()
        
        #対象のユーザーにリクエストを送信
        user_channel_name = receiver  # UserのWebSocketチャネル名を生成
        await self.channel_layer.send(
            user_channel_name,
            {
                "id" : sender
            }
        )