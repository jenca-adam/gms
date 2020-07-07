from django.db import models
from django.contrib.auth.models import User
class MAIL(models.Model):
    content=models.CharField(max_length=1000)
    from_user=models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='from_user')
    to_user=models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='to_user')
    datepub=models.DateTimeField(auto_now_add=True)
    attachment=models.FileField(upload_to='gmsapp/attachment/')
    def __str__(self):
        return('{}→{}:{}'.format(self.from_user.username,self.to_user.username,str(self.content)))




    
