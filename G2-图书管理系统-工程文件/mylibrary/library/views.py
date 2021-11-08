from django.http import Http404
from django.shortcuts import render,redirect
from .models import Book, Author, BookInstance
from django.views import View
from .forms import SearchForm
from django.contrib import messages

from .models import User,BookInstance,Book
# Create your views here.
from django.db.models import Q

from .models import is_over_date

from datetime import datetime, timedelta




def index(request):
    num_of_books = Book.objects.all().count()
    num_of_authors = Author.objects.count()
    context = {}
    context['num_of_books'] = num_of_books
    context['num_of_authors'] = num_of_authors
    return render(request,'index.html',context = context)


from django.views import generic

class BookListView(generic.ListView):
    model = Book
    #支持分页:
    paginate_by = 8 #当有8个以上的书籍时就采用分页显示
    template_name = 'book_list.html'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'





def book_detail_view(request,pk):
    try:
        book_id=Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("此书籍暂时不存在，可能是未上架或已下架")

    #book_id=get_object_or_404(Book, pk=pk)

    return render(
        request,
        'book_detail.html',
        context={'book':book_id,}
    )

class AuthorListView(generic.ListView):
    model = Author
    # 支持分页:
    paginate_by = 20  # 当有8个以上的书籍时就采用分页显示
    template_name = 'authors.html'


from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('date_back')



# LoginRequiredMixin提供登录状态验证，没有登录则跳转到login链接


class SearchView(LoginRequiredMixin,View):
    # login_url = 'accounts/login'

    def get(self,request):
        search = SearchForm(request.GET)
        if(search.is_valid()):
            keyword = search.cleaned_data['keyword']
            books = Book.objects.filter(Q(title__icontains=keyword)|Q(author__name__contains=keyword)|Q(pub__icontains=keyword))
            # books = BookInstance.objects.filter(Q(book__title__icontains=keyword)|Q(book__author__name__icontains=keyword)|Q(book__pub__icontains=keyword))
            if not books:
                message = '未查询到相关书籍'

        return render(request, "search.html", locals())



class BorrowView(LoginRequiredMixin,View):

    def get(self,request):
        if not request.user.is_authenticated:
            messages.error(request,'请先登录')
            return redirect('login')
        user_id = request.user.id
        book_id = request.GET.get('book_id')
        books = Book.objects.filter(id=book_id,is_aviliable=True)
        #设定还书最后期限为借书后的30天内
        if books:
            book = books.first()
            book.is_aviliable = False
            borrow_time = datetime.now()
            return_time = datetime.now()+timedelta(days=30)
            BookInstance.objects.create(borrower_id=user_id,book_id=book_id,status='o',date_borrow=borrow_time,date_back=return_time)
            messages.success(request,'借书成功')

            book.save()
        else:
            messages.error(request,'借书失败,书籍可能未上架')

        return redirect('search')



# 还书操作

class ReturnView(LoginRequiredMixin,View):

    def get(self,request):
        if not request.user.is_authenticated:
            messages.error(request,'请先登录')
            return redirect('login')

        user_id = request.user.id
        book_id = request.GET.get('book_id')
        borrowed_books_list = BookInstance.objects.filter(borrower_id=user_id)
        return_book  =  BookInstance.objects.filter(book_id = book_id,borrower_id=user_id)
        if borrowed_books_list:
            borrowed_book_return = borrowed_books_list.first()

            if is_over_date(borrowed_book_return):
                messages.warning(request,'已经逾期了,请缴纳罚款' )
            borrowed_book_return.delete()
            book = Book.objects.get(id = book_id)
            book.is_aviliable = True
            book.save()
            messages.success(request,'还书成功')
        else:
            messages.error(request,'还未借书')

        return redirect('my-borrowed')

# '>' not supported between instances of 'datetime.datetime' and 'NoneType'
