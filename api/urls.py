from django.urls import path
from . import views


urlpatterns = [
    path("sponsor-create/", views.SponsorCreateAPIView.as_view()),
    path("sponsor-list/", views.SponsorListAPIView.as_view()),
    path("sponsor-detail/<int:pk>/", views.SponsorDetailAPIView.as_view()),
    path("sponsor-update/<int:pk>/", views.SponsorUpdateAPIView.as_view()),
    path("student-sponsor/create/", views.StudentSponsorCreateAPIView.as_view()),
    path("student-list/", views.StudentListAPIView.as_view()),
    path("dashboard-statistic/", views.DashboardStatisticAPIView.as_view()),

    path("dashboard-graphic/", views.GraphicAPIView.as_view())
]
