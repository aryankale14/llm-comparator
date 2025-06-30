from django.contrib import admin
from .models import UserQuery

@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ("user", "query_text", "timestamp")
    search_fields = ("user__username", "query_text")
    list_filter = ("user", "model_used", "timestamp")
