from django.contrib import admin
from .models import Record

# To show Date Time in Admin
class DateTimeInAdmin(admin.ModelAdmin):
    readonly_fields = ('createdAt',)

# Register your models here.
admin.site.register(Record, DateTimeInAdmin)