from django.db import models
import datetime


# Create your models here.
class Article(models.Model):
    ariticle_id=models.IntegerField(primary_key=True)
    user_id=models.IntegerField()
    title=models.CharField(max_length=100,verbose_name='标题')
    content=models.TextField(max_length=5000,verbose_name='内容')
    date=models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'article'
        verbose_name = '博客'
        verbose_name_plural = verbose_name