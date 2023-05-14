from rest_framework import serializers
from core.models import TextModel, TagModel


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class SnippetSerializer(serializers.Serializer):
    text_snippet = serializers.CharField()
    tag = serializers.CharField()

class TextModelSerializer(serializers.ModelSerializer):

     class Meta:
        model = TextModel
        fields = '__all__'

class TagModelSerializer(serializers.ModelSerializer):

     class Meta:
        model = TagModel
        fields = '__all__'