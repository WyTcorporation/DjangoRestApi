from django.shortcuts import render
from .models import Article
from .serializers import ArticleModelSerializer
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404
from rest_framework.views import APIView

from rest_framework import mixins
from rest_framework import generics

from rest_framework import viewsets

# Authentication
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permisions import IsAuthor

'''
# 1 Standard
@csrf_exempt
def articles(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleModelSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        data = JSONParser().parse(request)
        serializer = ArticleModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def article(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArticleModelSerializer(article)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleModelSerializer(article, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)
'''

'''
# 2 https://www.django-rest-framework.org/tutorial/2-requests-and-responses/
# rest_framework method api_view
@api_view(['GET', 'POST'])
def articles(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleModelSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def article(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ArticleModelSerializer(article)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ArticleModelSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''

'''
# 3 https://www.django-rest-framework.org/tutorial/3-class-based-views/
class ArticleList(APIView):
    def get(self, request, format=None):
        snippets = Article.objects.all()
        serializer = ArticleModelSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ArticleModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetail(APIView):

    def get_object(self, slug):
        try:
            return Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        article = self.get_object(slug)
        serializer = ArticleModelSerializer(article)
        return Response(serializer.data)

    def put(self, request, slug):
        article = self.get_object(slug)
        serializer = ArticleModelSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        article = self.get_object(slug)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''

'''
# 4 Mixins https://www.django-rest-framework.org/tutorial/3-class-based-views/#using-mixins
class ArticleList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ArticleDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer
    lookup_field = 'slug'

    # Add author
    def perform_create(self,serializer_class):
                serializer_class.save(author=self.request.user)
                
    def get(self, request, slug, *args, **kwargs):
        return self.retrieve(request, slug=slug)

    def put(self, request, slug, *args, **kwargs):
        return self.update(request, slug=slug)

    def delete(self, request, slug, *args, **kwargs):
        return self.destroy(request, slug=slug)
'''

'''
# 5 Using generic class-based views
# https://www.django-rest-framework.org/tutorial/3-class-based-views/#using-generic-class-based-views
class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    lookup_field = 'slug'
    serializer_class = ArticleModelSerializer
'''


# https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/
class ArticleViewSet(viewsets.ViewSet):
    # Personal Authentication
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def list(self, request):
        article = Article.objects.all()
        serializer = ArticleModelSerializer(article, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArticleModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    lookup_field = 'slug'
    serializer_class = ArticleModelSerializer

    permission_classes = [IsAuthenticated,IsAuthor]
    authentication_classes = (TokenAuthentication, SessionAuthentication)