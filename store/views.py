from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    books=get_object_or_404(Book, pk=bid)
    count=BookCopy.objects.filter(books__exact=bid, status__exact=True).count()
    context = {
        'book':books , # set this to an instance of the required book
        'num_available':count , # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    return render(request, template_name, context=context)

@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }
    get_data = request.GET
    if get_data.count()>0:
        book=Book.objects.filter(title__icontains=get_data['title'], author__icontains=get_data['author'], genre__icontains=get_data['genre'])
    else:
        book=Book.objects.all()
    context['books']=book
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': None,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    get=BookCopy.objects.filter(borrower__exact=request.user)
    context['books']=get
    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    response_data = {
        'message': None,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    book_id =request.POST['bid']# get the book id from post data
    ref=BookCopy.objects.filter(book=book_id, status=True)
    if ref:
        book=ref[0]
        book.status=False
        book.borrower=request.user
        book.borrow_date=date.today()
        book.save()
        msg="success"
    else:
        msg="failure"
    response_data['message']=msg    
    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    response_data={
        'message':None,
    }
    book_id=request.POST['bid']
    book=BookCopy.objects.get(pk=book_id)
    try:
        book.borrower=None
        book.borrow_date=None
        book.status=True
        book.save()
        msg='success'
    except:
        msg='failure'
    response_data['message']=msg
    return JsonResponse(response_data)        



