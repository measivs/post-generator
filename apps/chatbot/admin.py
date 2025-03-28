from django.contrib import admin
from .models import Session, Chat
# Register your models here.

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('user',)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'sender', 'message', 'timestamp')
    list_filter = ('session', 'sender')
    search_fields = ('session', 'sender', 'message')
