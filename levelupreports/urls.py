from django.urls import path

from levelupreports.views.users.eventsbyuser import GamerEventList
from .views import UserGameList

urlpatterns = [
    path('reports/usergames', UserGameList.as_view()),
    path('reports/gamerevents',GamerEventList.as_view()),
]