from django.shortcuts import render
from .models import Link
from django.views import generic

# Create your views here.

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    num_links = Link.objects.all().count()

    return render(
        request,
        'index.html',
        context = {
            'num_links': num_links,
            },
    )

class LinkListView(generic.ListView):
    model = Link

    # queryset = Book.objects.all()

    # template_name = 'books/my_arbitrary_template_name_list.html'

# from .forms import LinkForm
#
# def new_link(request):
#     if request.method == 'POST':
#         form = LinkForm(request.POST)
#
#     return render(request, 'catalog/book_renew_librarian.html',
#         {'form': form,
#         'bookinst':book_inst}
#         )
