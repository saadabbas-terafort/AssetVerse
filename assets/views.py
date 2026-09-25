from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category , Frame , Sticker , Font , Effect , Slide
from .serializers import CategorySerializer , FrameSerializer , StickersSerializer , FontSerializers , EffectsSerializers , SlidesSerializers  
# Create your views here.
class CategoryView(APIView):
    def get(self , request):
        category = Category.objects.all()
        category = CategorySerializer(category , many=True)
        print(category)
        return Response(category.data)
    
class FrameView(APIView):
    def get(self , request):
        frame = Frame.objects.all()
        frame = FrameSerializer(frame , many=True)
        print(frame)

        return Response(frame.data)
    
    
class StickersView(APIView):
    def get(self , request):
        sticker = Sticker.objects.all()
        sticker = StickersSerializer(sticker , many=True)
        return Response(sticker.data)
    
class EffectView(APIView):
    def get(self , request):
        effect = Effect.objects.all()
        effect = EffectsSerializers(effect , many=True)
        return Response(effect.data)

class FontView(APIView):
    def get(self , request):
        font = Font.objects.all()
        font = FontSerializers(font , many=True)
        return Response(font.data)
    
class SlideView(APIView):
    def get(self , request):
        slide = Slide.objects.all()
        slide = SlidesSerializers(slide , many=True)
        return Response(slide.data)