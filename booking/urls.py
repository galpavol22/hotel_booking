from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import custom_login, index, about, gallery, kontakt, ubytovanie, create_reservation, reservation_detail, signup, room_detail, moj_ucet, cancel_reservation

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('gallery/', gallery, name='gallery'),
    path('kontakt/', kontakt, name='kontakt'),
    path('ubytovanie/', ubytovanie, name='ubytovanie'),
    path('login/', custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', signup, name='signup'),
    path('reservations/new/', create_reservation, name='create_reservation'),
    path('reservations/<int:reservation_id>/', reservation_detail, name='reservation_detail'),
    path('reservations/<int:reservation_id>/cancel/', cancel_reservation, name='cancel_reservation'),
    path('room/<int:room_id>/', room_detail, name='room_detail'),
    path('moj_ucet/', moj_ucet, name='moj_ucet'),
]
