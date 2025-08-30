from rest_framework import routers, serializers, viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(published=True)
    serializer_class = BookSerializer

router = routers.DefaultRouter()
router.register(r'book/list', BookViewSet) #ลงทะเบียน API สำหรับรายการหนังสือ