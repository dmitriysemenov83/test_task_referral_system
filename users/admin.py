from django.contrib import admin

from users.models import User, Referral

admin.site.register(User)

admin.site.register(Referral)
