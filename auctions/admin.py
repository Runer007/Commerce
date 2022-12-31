from django.contrib import admin

from .models import User, Auction,  Coment, Stavca

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("auctions", )

admin.site.register(Auction)
admin.site.register(User, UserAdmin)
admin.site.register(Coment)
admin.site.register(Stavca)