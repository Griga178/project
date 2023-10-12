from .parser_core import get_page, find_content, string_to_float, string_to_float, clean_string

from .models import Link, Parse_result

def parse_link(link_id):

    link_obj = Link.objects.get(id = link_id)

    html_page = get_page(link_obj.name)

    settings = []
    for setting in link_obj.domain.domain_setting_set.all():
        content = find_content(html_page, setting)

        parse_content = Parse_result(
        link = link_obj,
        domain_setting = setting,
        value = content
            )
        parse_content.save()

        print(content)
        print(parse_content)

    return parse_content
