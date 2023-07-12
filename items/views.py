from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .serializers import *


@api_view(['GET', 'POST'])
def items_list(request):
    """
 List items, or create a new item.
 """
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        items = Items.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(items, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = ItemsSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()
        
        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/items/?page=' + str(nextPage), 'prevlink': '/api/items/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = ItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def items_detail(request, pk):
    try:
        item = Items.objects.get(pk=pk)
    except Items.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ItemsSerializer(Items,context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # try:
        data = request.data
        item = Items.objects.get(pk=data.get('pk'))
        photo = request.FILES["photo"]
        item.title=data.get('title')
        item.content= data.get('content')
        item.price= data.get('price')
        item.stock = data.get('stock')
        item.available = data.get('available')
        item.photo= photo
        item.save()
        response = {"result":'Item Updated Sucessfully'}
        return Response(response)
        # except:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
