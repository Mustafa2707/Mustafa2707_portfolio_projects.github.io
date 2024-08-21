from django.contrib import admin
from auctions.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(Bid)
admin.site.register(SubCategory)
admin.site.register(Image)
admin.site.register(Watchlist)
