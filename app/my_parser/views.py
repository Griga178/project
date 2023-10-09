from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Link
from .forms import LinkFormSet

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

    template_name = "my_parser/link_list.html"



class LinkAddView(generic.TemplateView):
    template_name = "my_parser/add_link.html"

    def get(self, *args, **kwargs):
        formset = LinkFormSet(queryset = Link.objects.none())

        return self.render_to_response({'link_formset': formset})

    def post(self, *args, **kwargs):

        formset = LinkFormSet(data = self.request.POST)

        if formset.is_valid():
            formset.save()

            return redirect(reverse_lazy("links"))

        return self.render_to_response({'link_formset': formset})
