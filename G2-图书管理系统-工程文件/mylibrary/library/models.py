from django.db import models
import uuid
# Create your models here.
from datetime import datetime, timedelta
from django.urls import reverse

from django.contrib.auth.models import User
from datetime import date

#定义图书模型:
#并添加字段定义（字段相当于数据库表中的列属性）
from django.views import generic


class Book(models.Model):
    #书名
    title = models.CharField(max_length=50)
    #作者
    author = models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)
    is_aviliable = models.BooleanField(verbose_name='是否可借', default=True)

    #出版社
    pub = models.CharField(max_length=30)
    #概述
    summary = models.TextField(help_text='写一些对此书的概述吧')

    def __str__(self):
        return "<书名:%s>"%self.title#返回当前对象的书名，显示在管理页面上
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('book-detail', args=[str(self.id)])
class Author(models.Model):

    name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # date_of_birth = models.DateField(null=True, blank=True)
    # date_of_death = models.DateField('Died', null=True, blank=True)

    # def get_absolute_url(self):
    #     """
    #     Returns the url to access a particular author instance.
    #     """
    #     return reverse('author-detail', args=[str(self.id)])


    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.name)

#图书的副本，用于定义此书籍是可借。预计的返还日期等信息
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    book = models.ForeignKey('Book',on_delete=models.SET_NULL,null=True)
    date_borrow = models.DateTimeField(null=True,blank=True)
    date_back = models.DateTimeField(null=True,blank=True)
    #书籍借阅状态
    LOAN_STATUS = (
        ('m', 'Maintenance(未上架)'),
        ('o', 'On loan(被借)'),
        ('a', 'Available(可借)'),
        # ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id,self.book.title)
    #根据返还日期排序
    class Meta:
        ordering = ["date_back"]

# @admin.register(BookInstance)
# class BookInstanceAdmin(admin.ModelAdmin):
#     list_display = ('book', 'status', 'borrower', 'due_back', 'id')
#     list_filter = ('status', 'due_back')
#
#     fieldsets = (
#         (None, {
#             'fields': ('book','imprint', 'id')
#         }),
#         ('Availability', {
#             'fields': ('status', 'due_back','borrower')
#         }),
#     )




#借的书籍是否逾期
# @property
def is_over_date(self):
    if self.date_back.replace(tzinfo = None) and datetime.now().replace(tzinfo=None)>self.date_back.replace(tzinfo = None):
        return True
    return False

