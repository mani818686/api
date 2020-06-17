from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from api_basics.serializers import ArticleSerializer
from api_basics.models import Article
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,filters
from django.shortcuts import get_object_or_404
import django_filters.rest_framework

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class=ArticleSerializer
    queryset=Article.objects.all()
    filterset_fields ='__all__'
    #filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends=[filters.OrderingFilter]
    search_fields=['id','author','email','title','date']

#viewsets.GenericViewSet,mixins.ListModelMixin,
# mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin-------> fro generic viewsets
''' def list(self,request):
        articles=Article.objects.all()
        serializer=ArticleSerializer(articles,many=True)
        return Response(serializer.data)

    def create(self,request):
        serializer=ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        queryset=Article.objects.all()
        article=get_object_or_404(queryset,pk=pk)
        serializer=ArticleSerializer(article)
        return Response(serializer.data)
    
    def update(self,request,pk=None):
        article=Article.objects.get(pk=pk)
        serializer=ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)'''
    # end of viewsets.viewset-->
    

    






class GenericAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class=ArticleSerializer
    queryset=Article.objects.all()
    lookup_field='id'
    authentication_classes=[SessionAuthentication,BasicAuthentication]
    #authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)
    def post(self,request,id=None):
        return self.create(request,id)
    def put(self,request,id=None):
        return self.update(request,id)
    def delete(self,request,id=None):
        return  self.destroy(request) 

class ArticleAPIView(APIView):

    def get(self,request):
        articles=Article.objects.all()
        serializer=ArticleSerializer(articles,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ArticleDetail(APIView):
    def get_object(self,id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request,id):
        article=self.get_object(id)
        serializer=ArticleSerializer(article)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def put(self,request,id):
        article=self.get_object(id)
        serializer=ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            #return JsonResponse(serializer.data,status=201)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        article=self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



















@api_view(['GET','POST'])
#@csrf_view
def article_list(request):
    if request.method=="GET":
        articles=Article.objects.all()
        serializer=ArticleSerializer(articles,many=True)
        #return JsonResponse(serializer.data,safe=False)
        return Response(serializer.data)
    
    else:
        #data=JSONParser().parse(request)
        #serializer=ArticleSerializer(data=data)
        serializer=ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#@csrf_exempt
@api_view(['PUT','GET','DELETE'])
def article_detail(request,pk):
    try:
        article=Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        #return HttpResponse(status=404)
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer=ArticleSerializer(article)
        #return JsonResponse(serializer.data,safe=False)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    elif request.method=='PUT':
        #data=JSONParser().parse(request)
        #serializer=ArticleSerializer(article,data=data)
        serializer=ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            #return JsonResponse(serializer.data,status=201)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        article.delete()
        #return HttpResponse(status=204)
        return Response(status=status.HTTP_204_NO_CONTENT)

