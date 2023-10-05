import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import RequestForLoverModel
import channels.layers
from asgiref.sync import async_to_sync
import asyncio

class RequestConsumer(AsyncWebsocketConsumer):
    
    #idとchannel名が辞書として保存された辞書をキューグループの代わりとして使う、スケーラビリティを考慮したイベントハンドリングをする
    
    channel_id_mapping: dict[int, str]
    #channel名からuser_idを抽出する
    user_id: int = 39
    
    #websocket接続を開始したら辞書にchannelを保存する
    #idが自身のidで、isRequestSentがFalseであるリクエストを探す、ヒットしたら全て送信する
    async def connect(self) -> None: 
        self.accept() 
        await self.save_channel_with_id() 
        
    #websocket接続を切断したらキューから対象channelを削除する
    async def disconnect(self, close_code) -> None:
        await self.delete_channel_with_id()
        
    #メッセージを受信し、DBに保存
    async def receive(self, text_data) -> None:
        data = json.loads(text_data) 
        content :str = data['content']
        if content=="MatchingRequest":
            self.processMatchingRequest(data)
        if content=="ReceiptConfirmation":
            self.receive_confirmation_catchrequest(data)
        
            
    async def processMatchingRequest(self, data) ->None:
        sender = data['sender']
        receiver = data['receiver']
        request_message = data['request_message']
        
        if not sender or not receiver:
            await self.send(text_data=json.dumps({'error': 'Incomplete data received'}))
            return
       
        message = RequestForLoverModel(sender=sender, receiver=receiver)
        message.save()
       
        if self.user_id in self.channel_id_mapping:
            user_channel_name = self.channel_id_mapping[self.user_id]
            await self.send_request(user_channel_name, sender, request_message)
            
    async def save_channel_with_id(self) -> None:
        self.channel_id_mapping[self.user_id] = self.channel_name
    
    async def delete_channel_with_id(self) -> None:
        del self.channel_id_mapping[self.user_id]
    
    
    #websocket通信でrequestを送信
    async def send_request(self, user_channel_name, sender, request_message) -> None:
        try:
            self.channel_layer.send(
                user_channel_name,
                {
                    "id" : sender,
                    "request_message" : request_message
                }
            )
        except Exception as e:
            print(f"例外が発生しました:{e}")
            
    
    #receiverからの受け取ったことを伝えるメールを確認するコードを書く
    #それを受け取って完了する->isRequestSentをtrueに変更する、メールが消失した場合、誤配信のエラーハンドリングを行う
    async def receive_confirmation_catchrequest(self, data) ->None:
        pass
                
    