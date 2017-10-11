from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from scraper.serializers import ArtistSerializer, SongSerializer
from scraper.models import Artist, Song


class ArtistViewSet(ViewSet):

    def list(self, request):
        queryset = Artist.objects.all()
        serializer = ArtistSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Artist.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ArtistSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            return Response(status=404)
        serializer = ArtistSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class SongViewSet(ViewSet):

    def list(self, request):
        queryset = Song.objects.all()
        serializer = SongSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Song.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = SongSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response(status=404)
        serializer = SongSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)
