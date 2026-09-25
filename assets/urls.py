from django.contrib import admin
from django.urls import path , include
from .views import CategoryView , FrameView , SlideView , FontView , StickersView
urlpatterns = [
    path('api/category' ,CategoryView.as_view() , name="category" ),
    path('api/frame' , FrameView.as_view() , name="frame"),
    path('api/effect', SlideView.as_view() , name="effect"),
    path('api/font' ,FontView.as_view() , name="font"),
    path('api/sticker' , StickersView.as_view() , name="sticker" ),

]
