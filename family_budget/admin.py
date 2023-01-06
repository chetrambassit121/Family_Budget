from django.contrib import admin
from .models import Project, Expense, Category


admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Expense)

