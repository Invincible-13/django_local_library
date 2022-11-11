from turtle import title
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Book,BookInstance,Language,Author,Genre
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from .forms import RenewBookModelForm
import datetime
from django.views.generic.edit import DeleteView, CreateView, UpdateView
# from djano.Htt

# Create your views here.
@login_required
def index(request):
    # Counts
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_books_search = Book.objects.filter(title__icontains='th').count()
    # available books
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_authors' : num_authors,
        'num_genres' : num_genres,
        'num_books_search' : num_books_search,
        'num_visits' : num_visits
    }
    return render(request, 'index.html', context)

class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
    paginate_by = 4
    #overriding the defaults
    # context_object_name = 'my_name' // default: object_list or book_list
    # template_name = 'book_list.html'
    # queryset = Book.objects.filter(title__icontains='war')[:5]
    # OR
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5]
    # Pass additional context
    # def get_context_data(self, **kwargs):
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     context['some_data'] = 'This is some data.'
    #     return context

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(LoginRequiredMixin,generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    model = BookInstance
    paginate_by = 4

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class ViewBorrowedBooks(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/all_borrowed_books.html'
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.all()

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookModelForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['due_back']
            book_inst.save()
            return HttpResponseRedirect(reverse('borrowed'))
    else:
        def_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back' : def_date})

    context = {
        'form' : form,
        'book_instance' : book_inst,
    }
    return render(request, 'catalog/book_renew_librarian.html', context)
        
class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death' : '11/06/2020'}

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('author_list')

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__'

class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    success_url = reverse_lazy('book_list')

# class MyView(LoginRequiredMixin, View):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'

# @login_required
# # request.user.is_authenticated
# def BookListView(request):
#     book_list = Book.objects.all()
#     context = {
#         'book_list' : book_list
#     }
#     return render(request,'catalog/book_list.html', context)

# def BookDetailView(request, pk):
#     book_id = Book.objects.get(pk=pk)
#     genre_id = Genre.objects.get(pk=pk)
#     context = {
#         'book_id' : book_id,
#         'genre_id' : genre_id
#     }
#     return render(request, 'book_detail.html', context)

# def AuthorListView(request):
#     authors_all = Author.objects.all()
#     context = {
#         'authors_all' : authors_all
#     }
#     return render(request, 'author_list.html', context)

# def AuthorDetailView(request, id):
#     author_id = Author.objects.get(id=id)
#     context = {
#         'author_id' : author_id
#     }
#     return render(request, 'author_detail.html', context)

