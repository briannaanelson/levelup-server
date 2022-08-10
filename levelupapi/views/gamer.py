from dataclasses import fields
from django.http import HttpResponseServerError
from django.views import View
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Gamer
from levelupapi.models.game import Game


class GamerView(ViewSet):
    def retrieve(self, request, pk):
        gamer = Gamer.objects.get(pk=pk)
        serializer = GamerSerializer(gamer)
        return Response(serializer.data)
    
    def list(self, request):
        gamer = Gamer.objects.all()
        serializer = GamerSerializer(gamer, many=True)
        return Response(serializer.data)
    
class GamerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamer
        fields = ('id', 'user', 'bio')