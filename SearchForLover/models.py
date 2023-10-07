from django.db import models
from profiling.models import UserProfile

# Create your models here.
class RequestForLoverModel(models.Model):
    '''
    受け取るユーザーのid, nickname, 送るユーザーのid, nickname, メッセージ、リクエストが送られた日時、
    リクエストの状態のmodel
    '''
    receiver = models.ForeignKey(UserProfile, related_name = 'receiver', on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, related_name= 'sender', on_delete=models.CASCADE)
    request_message = models.TextField(blank = True)
    STATUS_CHOICES =(
        ('PENDING', '承認待ち'),
        ('APPROVED', '承認'),
        ('REJECTED', '拒否'),
    )
    status = models.CharField(max_length=10, choices = STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'SearchForLover'
        
    def __str__(self):
        return f"Request from {self.sender} to {self.receiver}: {self.status}"

class UnsentRequestModel(models.Model):
    '''
    senderのid, receiverのid, senderのnickname, receiverのnickname, senderからのmessage、
    senderがリクエストした日にちを入れる
    '''
    receiver = models.ForeignKey(UserProfile, related_name = 'receiver', on_delete=models.CASCADE)
    receiver_nickname = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    sender = models.ForeignKey(UserProfile, related_name= 'sender', on_delete=models.CASCADE)
    sender_nickname = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    request_message = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)