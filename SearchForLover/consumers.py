import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import RequestForLoverModel
import channels.layers
from asgiref.sync import async_to_sync
import asyncio

class RequestConsumer(AsyncWebsocketConsumer):
    
    #idとchannel名が辞書として保存された辞書をキューグループの代わりとして使う、スケーラビリティを考慮したイベントハンドリングをする
    
    channel_id_mapping ={}
    user_id = 39
    
    
    async def save_channel_with_id(self):
        self.channel_id_mapping[self.user_id] = self.channel_name
    
    async def delete_channel_with_id(self):
        del self.channel_id_mapping[self.user_id]
    
    #websocket接続を開始したら辞書にchannelを保存する
    #待機中のリクエストから接続したユーザー向けのリクエストを探す
    async def connect(self): 
        await self.accept() 
        await self.save_channel_with_id()
        '''リクエストを探す'''
        

    #websocket接続を切断したらキューから対象channelを削除する
    async def disconnect(self, close_code):
        await self.delete_channel_with_id()
    
    #websocket通信でrequestを送信
    async def send_request(self, user_channel_name, sender, request_message):
        try:
            self.channel_layer.send(
                user_channel_name,
                {
                    "id" : sender,
                    "request_message" : request_message
                }
            )
            '''
            ここにreceiverからの受け取ったことを伝えるメールを確認するコードを書く
            それを受け取って完了する、メールが消失した場合、誤配信のエラーハンドリングを行う
            '''
        #この例外処理はメッセージを送信したが正常に
        except Exception as e:
            print(f"例外が発生しました:{e}")
                
    
    async def receive(self, text_data):
        #メッセージを受信し、DBに保存
        # バリデーションをでシリアライズした後行う
        data = json.loads(text_data) #json.loadsでデシリアライズ
        sender = data['sender']
        receiver = data['receiver']
        request_message = data['request_message']
        
        if not sender or not receiver:
            await self.send(text_data=json.dumps({'error': 'Incomplete data received'}))
            return
       
        message = RequestForLoverModel(sender=sender, receiver=receiver)
        message.save()
        
        '''
        対象のユーザーにリクエストを送信,対象のユーザーがwebsocket接続しているならばその場で送信、リクエストのリストに保存する...その場で送信が失敗したら？？
        検索対象ユーザーのidからチャネル名を検索する
        '''
       
        if self.user_id in self.channel_id_mapping:
            user_channel_name = self.channel_id_mapping[self.user_id]
            await self.send_request(user_channel_name, sender, request_message)