from django.contrib import admin
from .models import Book
from .models import Author
from .models import BookInstance
# Register your models here.

#注册模型：
# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookInstance)

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower','date_borrow','date_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'date_back','borrower')
        }),
    )
