from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('registration', views.registration, name='registration'),
    path('get_dealers', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_detail'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
    path('add_review', views.add_review, name='add_review'),
    path('get_cars', views.get_cars, name='get_cars'),
]
