
from django.urls import include, path, re_path
from rest_framework import routers
from matchingapp_project.quickstart import views
from authentication.views import CheckUsernameView, UserLoginView
from profiling.views import SchoolNameView, AccountRegistrationView, ProfileRegistrationView
from account_check.views import IDfromTokenView, AccountInfoFromIDView, ChangeProfileInfoView
from SearchForLover.views import GetRecommendation, GetRequestView

urlpatterns = [
    path('api/login/', UserLoginView.as_view(), name='login'),
    path('api/check_user/', CheckUsernameView.as_view(), name='account-check'), 
    path('api/school/', SchoolNameView.as_view(), name='school-create'),
    path('api/account_register/', AccountRegistrationView.as_view(), name='account-create'),
    path('api/profile_register/', ProfileRegistrationView.as_view(), name='profile-create'),
    path('api/account_check/', IDfromTokenView.as_view(), name='account-check'),
    path('api/get_accountinfo/',AccountInfoFromIDView.as_view(), name="get-accountinfo"),
    path('api/change_accountinfo/',ChangeProfileInfoView.as_view(), name="change-accountinfo"),
    path('api/get_recommendation/',GetRecommendation.as_view(), name='get-recommendation'),
]

