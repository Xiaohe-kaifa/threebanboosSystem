"""
URL configuration for threebanboos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from app01.views import LoginView,peopleLogin,idBusinessLogin,delCartView,cartDetailView,manageLogin,cartView,manageCloseLogin,ChatMessageView,peopleCloseLogin,homeNumberView, chart02View,chart01View,ordersSystemDetailView,ordersSystemCountView,ordersView,ordersSystemView,commoditySearchPeopleTableView,CommodityDetailView,commoditySearchTypeView,commoditySearchView,commoditySearchCountView,agreeBusinessDetailView,CommodityView,ChatSearchCountView,ChatSearchView,ChatMessageDetailView,ChatPeopleDetailView,LoginDetailView,SearchDetailView,LunBoTuView,LunBoTuDetailView,avatarView, businessSearchCountView, businessSearchView,verifyView,successView,suggestionView,suggestionDetailView,searchSuggestionView,returnPhotoView,businessView
from django.urls import path,re_path
from app01 import views
urlpatterns = [
    path('api/login/',LoginView.as_view()),
    re_path('api/login/(\d+)',LoginDetailView.as_view()),
    path('api/search/',SearchDetailView.as_view()),
    path('api/lunbotu/',LunBoTuView.as_view()),
    re_path('api/lunbotu/(\d+)',LunBoTuDetailView.as_view()),
    path('api/avatar/',avatarView.as_view()),
    path('api/verify/',verifyView.as_view()),
    path('api/success/',successView.as_view()),
    path('api/suggestion/',suggestionView.as_view()),
    re_path('api/suggestion/(\d+)',suggestionDetailView.as_view()),
    path('api/searchSuggestion/',searchSuggestionView.as_view()),
    path('api/returnPhoto/',returnPhotoView.as_view()),
    path('api/business/',businessView.as_view()),
    path('api/businessSearch/',businessSearchView.as_view()),
    path('api/businessSearchCount/',businessSearchCountView.as_view()),
    re_path('api/agreeBusiness/(\d+)',agreeBusinessDetailView.as_view()),
    path('api/chatMessage/',ChatMessageView.as_view()),
    re_path('api/chatMessage/(\d+)',ChatMessageDetailView.as_view()),
    re_path('api/chatPeople/(\d+)',ChatPeopleDetailView.as_view()),
    path('api/chatMessageSearch/',ChatSearchView.as_view()),
    path('api/messageSearchCount/',ChatSearchCountView.as_view()),
    path('api/commodity/',CommodityView.as_view()),
    path('api/searchCommodityCount/',commoditySearchCountView.as_view()),
    path('api/searchCommodity/',commoditySearchView.as_view()),
    re_path('api/commodity/(\d+)',CommodityDetailView.as_view()),
    path('api/searchCommodityType/',commoditySearchTypeView.as_view()),
    path('api/searchCommodityPeopleTable/',commoditySearchPeopleTableView.as_view()),
    path('api/orders/',ordersView.as_view()),
    path('api/ordersSystem/',ordersSystemView.as_view()),
    path('api/ordersSystemCount/',ordersSystemCountView.as_view()),
    re_path('api/ordersSystem/(\d+)',ordersSystemDetailView.as_view()),
    path('api/chart01/',chart01View.as_view()),
    path('api/chart02/',chart02View.as_view()),
    path('api/homeNumber/',homeNumberView.as_view()),
    path('api/peopleLogin/',peopleLogin.as_view()),
    path('api/peopleCloseLogin/',peopleCloseLogin.as_view()),
    path('api/manageLogin/',manageLogin.as_view()),
    path('api/manageCloseLogin/',manageCloseLogin.as_view()),
    path('api/idBusiness/',idBusinessLogin.as_view()),
    path('api/cart/',cartView.as_view()),
    re_path('api/cart/(\d+)',cartDetailView.as_view()),
    path('api/delCart/',delCartView.as_view()),
]
