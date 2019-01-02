from django.db import models
from register.models import Users
import datetime


# Create your models here.
class Article(models.Model):
    ariticle_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100,verbose_name='标题')
    content=models.TextField(max_length=5000,verbose_name='内容')
    date=models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))

    user=models.ForeignKey(Users,null=True)


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'article'
        verbose_name = '博客'
        verbose_name_plural = verbose_name


class Article_tag(models.Model):
    tag_id=models.AutoField(primary_key=True)
    tag=models.CharField(max_length=20)

    article=models.ManyToManyField(Article,null=True)


    def __str__(self):
        return self.tag

    class Meta:
        db_table='article_tag'
        verbose_name='标签'
        verbose_name_plural=verbose_name