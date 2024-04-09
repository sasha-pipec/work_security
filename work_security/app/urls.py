from django.urls import path

from app.views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('authorization/', AuthorizationPageView.as_view(), name='authorization'),
    path('registration/', RegistrationPageView.as_view(), name='registration'),
    path('logout/', user_logout, name='logout'),
    path('personal_area/', PersonalAreaPageView.as_view(), name='personal_area'),
    path('tests/', TestsPageView.as_view(), name='tests'),

    path('instructions/<int:id>/', InstructionDetailView.as_view(), name="instruction_detail"),
    path('tests/<int:id>/', TestDetailView.as_view(), name="test_detail"),

    path('get_score_for_test/<int:id>/', GetScoreForeTestView.as_view(), name="get_score")
]
