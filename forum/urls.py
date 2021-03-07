from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('threadlist/<int:forum>', ThreadlistView.as_view(), name='threadlist'),
    path('viewthread/<int:thread>', ViewThreadView.as_view(), name='viewthread'),
    path('newthread/<int:forum>', NewThreadView.as_view(), name='newthread'),
    path('memberlist', MemberlistView.as_view(), name='memberlist'),
    path('member/<int:userid>', UserProfileView, name='member'),
    path('usercp/', UserCPView.as_view(), name='usercp'),
    path('search/', SearchView.as_view(), name='search'),
    path('search/results/kw=<str:keywords>-author=<str:author>', SearchResultsView.as_view(), name='search-results'),
]