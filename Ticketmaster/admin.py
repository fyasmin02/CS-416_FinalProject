from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Userprofile


# unregistered groups from admin panel
admin.site.unregister(Group)


# add profile into user section
class ProfileInLine(admin.StackedInline):
    model = Userprofile


# modifying user model in admin panel
class UserAdmin(admin.ModelAdmin):
    model = User
    # only display username
    fields = ["username"]
    inlines = [ProfileInLine]


# unregister initial user
admin.site.unregister(User)

# re-register user
admin.site.register(User, UserAdmin)


# add profile into user section
class ProfileInLine(admin.StackedInline):
    model = Userprofile





