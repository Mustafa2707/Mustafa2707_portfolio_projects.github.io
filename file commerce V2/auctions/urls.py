from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Create/Listing",views.create_listing,name='create_listing'),
    path("Watchlist/User=<int:user_id>",views.display_watchlist,name='display_watchlist'),
    path('Watchlist/Listing=<int:listing_id>/User=<int:user_id>/Toggle',views.Toggle_Watchlist_status,name='Toggle_Watchlist_status'),
    path("Categories/view",views.display_categories,name='display_categories'),
    path("Cart/User=<int:user_id>",views.display_cart,name='display_cart'),
    path("Cart/Added/Listing=<int:listing_id>",views.Cart_Listing,name='Cart_Listing'),
    path('View/Listing_ID=<int:listing_id>/Listing_Title=<str:listing_title>/',views.display_listing,name='display_listing'),
    path("Place/Bid/Listing=<int:listing_id>/Bidder=<int:Bidder_id>",views.Place_Bid,name="Place_Bid"),
    path("Place/Comment/Listing=<int:listing_id>/Commenter=<int:commenter_id>",views.Place_Comment,name="Place_Comment"),
    path('Add/Image/Listing=<int:listing_id>',views.Add_Image,name="Add_Image")
]
