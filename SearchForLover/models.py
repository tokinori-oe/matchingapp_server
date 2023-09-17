from django.db import models
from profiling.models import UserProfile

# Create your models here.
class RequestForLoverModel(models.Model):
    #受け取るユーザー
    receiver = models.ForeignKey(UserProfile, related_name = 'received_requests', on_delete=models.CASCADE)
    
    #送るユーザー
    sender = models.ForeignKey(UserProfile, related_name= 'sent_requests', on_delete=models.CASCADE)
    
    #リクエストの状態
    STATUS_CHOICES =(
        ('PENDING', '承認待ち'),
        ('APPROVED', '承認'),
        ('REJECTED', '拒否'),
    )
    
    status = models.CharField(max_length=10, choices = STATUS_CHOICES, default='PENDING')
    
    #リクエストの作成日時
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'SearchForLover'
        
    def __str__(self):
        return f"Request from {self.sender} to {self.receiver}: {self.status}"
    
    #def __str__(self):
        #return self.user.username #ユーザー名を返すことでプロフィールを識別
