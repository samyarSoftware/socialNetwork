from django.contrib import admin
from .models import User, Post, Comment, Ticket, TicketReply
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(User)
class UsersAdmin(UserAdmin):
    list_display = ['username', 'phone', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {'fields': ['job', 'bio', 'date_of_birth', 'phone', 'photo']}),
    )


@admin.action(description="غیر فعال کردن پست")
def deactivate(modeladmin, request, queryset):
    update = queryset.update(active = False)
    message = f"{update} post was deactivated" if len(update) == 1 else f"{update} posts were deactivated"
    modeladmin.message_user(request, message)


@admin.register(Post) 
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'description', 'created']
    ordering = ['-created']
    list_filter = ['created', 'author']
    search_fields = ['description', 'author']
    raw_id_fields = ['author']
    date_hierarchy = 'created'
    actions = [deactivate]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'body', 'created']
    ordering = ['-created', 'author']
    list_filter = ['created', 'author', 'body']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject']
    ordering = ['-created']
    


@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'text']