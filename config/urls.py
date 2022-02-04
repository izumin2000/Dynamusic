from django.contrib import admin
from django.urls import path
from Dynamusic import views


urlpatterns = [
    path('', views.index, name='index'),
    path('autoplay/<int:beats>', views.autoplay, name='autoplay'),
    path('<int:beats>', views.tobeats, name='tobeats'),
    path('<int:beats>/', views.edit, name='edit'),
    path('chat/', views.chat, name='chat'),
    path('chat/<int:beats>', views.chatbeats, name='chatbeats'),
    path('doc', views.doc, name='doc'),
    path('midis/', views.midis, name='midis'),
    path('initsound/',views.initsound,name='initsound'),
    path('initchat/', views.initchat, name='initchat'),
    path('terms/', views.terms, name='terms'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('create/', views.UserCreateView.as_view(), name="create"),
    path('admin/', admin.site.urls),
]
    # path('mypage/<str:username>', views.mypage, name='mypage'),
