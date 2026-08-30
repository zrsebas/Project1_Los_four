from django.contrib import admin
from .models import Movie

# Register your models here.
admin.site.register(Movie)
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
	list_display = ('title', 'published')
	search_fields = ('title', 'desc')