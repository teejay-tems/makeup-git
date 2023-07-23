from rest_framework import generics, status
from rest_framework.response import Response
from .models import MenuItem, Category
from .serializers import MenuItemiSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
# for pagenation
from django.core.paginator import Paginator, EmptyPage




class CategoryView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = Category

# function based
@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        # filter per field
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        # search filter
        search = request.query_params.get('search')

        # ordering filter
        ordering = request.query_params.get('ordering')

        # for pagenation filter
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        
        #filtering items 
        """
        127.0.0.1:8000/api/menu-item1?category_name=beverages
        """
        if category_name:
            items = items.filter(category__title=category_name)
        """
        127.0.0.1:8000/api/menu-item1?to_price=120
        """
        if to_price:
            items = items.filter(price=to_price)
        """
        127.0.0.1:8000/api/menu-item1?search=tilapia
        """
        if search:
            items = items.filter(title__icontains=search)
        """
        
        """
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
        
        # initiating paginator object
        paginator = Paginator(items, per_page=perpage)
        """
        Try these:
        127.0.0.1:8000/api/menu-item1
        127.0.0.1:8000/api/menu-item1?perpage=3&page=1
        """
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

        serialized_item = MenuItemiSerializer(items, many=True)
        return Response(serialized_item.data)
    if request.method == 'POST':
        serialized_item = MenuItemiSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.validated_data, status.HTTP_201_CREATED)

@api_view()
def single_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    serialized_item = MenuItemiSerializer(item)
    return Response(serialized_item.data)

# class based
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemiSerializer

    

class SingleItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemiSerializer

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)