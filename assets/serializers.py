from rest_framework import serializers 
from .models import Category , Frame , Sticker , Effect , Font , Slide

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
        
class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = '__all__'
    
class StickersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = '__all__'
        
class EffectsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Effect
        fields = '__all__'
        
        
class FontSerializers(serializers.ModelSerializer):
    class Meta:
        model = Font
        fields = '__all__'
        

class SlidesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = '__all__'