from django.contrib import admin

# Register your models here.
from .models import Link, Domain, Domain_setting, Parse_result

admin.site.register(Link)
admin.site.register(Domain)
admin.site.register(Domain_setting)
admin.site.register(Parse_result)
