from django.contrib import admin
from knn_model.models import User,History, Message

# Register your models here.

# class UserApp(admin.ModelAdmin):
#     list_display = ['id_user', 'username', 'email', 'password']
#     search_fields = ['username', 'email']

class HistoryPlay(admin.ModelAdmin):
    list_display = ['id_history','id_user','hero_name', 'hero_damage', 'turret_damage', 'damage_taken', 'war_participation', 'result']
    search_fields = ['hero_name','result']

class MessageUser(admin.ModelAdmin):
    list_display = ['id_message', 'id_user', 'message']
    search_fields = ['id_message', 'id_user', 'message']

# admin.site.register(User, UserApp)

admin.site.register(History, HistoryPlay)

admin.site.register(Message, MessageUser)

# class YourAdmin(admin.ModelAdmin):
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):                
#         if db_field.name == 'user': kwargs['queryset'] = User.objects.filter(user=request.user)