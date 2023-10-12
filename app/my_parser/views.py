from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Link
from .forms import LinkFormSet
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import json

from .parser_core import get_page, find_content, string_to_float
from .parser_func import parse_link
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

@require_POST
def parse(request):
    if request.method == 'POST':
        user = request.user
        link_id = request.POST.get('link_id', None)

        parse_link(link_id)
        # link_obj = Link.objects.get(id = link_id)

        # html_page = get_page(link_obj.name)

        # dirty_settings = link_obj.domain.domain_setting_set.all()
        # # print(dirty_settings)
        # settings = []
        # for el in dirty_settings:
        #     setting = {
        #         "content_type": el.content_type,
        #         "tag": el.tag,
        #         "attr": el.attr,
        #         "attr_val": el.attr_val,
        #         }
        #     settings.append(setting)
        # # print(settings)
        # content = find_content(html_page, settings)
        # print(content)
        # message = f'You wonna parse link with id: {link_obj}'
        # message = {'a':f"Price: {content['price']}, name: {content['name']}"}

    ctx = {'message': "hello =)"}
    return HttpResponse(json.dumps(ctx), content_type='application/json')

class LinkDetailView(generic.DetailView):
    model = Link

    template_name = "my_parser/link_page.html"

class LinkListView(generic.ListView):
    '''
        Смотрим на список ссылок
    '''
    model = Link

    template_name = "my_parser/link_list.html"



class LinkAddView(generic.TemplateView):
    '''
        Добавляем 1(+) ссылку
    '''
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
