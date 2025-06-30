from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("analytics/", views.analytics, name="analytics"),
    path("dashboard/query/<int:query_id>/", views.query_detail, name="query_detail"),
]
