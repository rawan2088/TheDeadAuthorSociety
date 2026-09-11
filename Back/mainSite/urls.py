from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include('users.urls')),
    # path('api/books/', include('books.urls')),
    path('api/', include('borrowed.urls')),
    path("api/", include("books.urls")),  
    path('silk/', include('silk.urls', namespace='silk')),  # for API documentation
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# This makes Django serve files at http://127.0.0.1:8000/media/book_covers/book1.webp.

# in django we use this path
# book_covers/book1.webp
#  request.build_absolute_uri(books.image.url) turns it into:
# http://127.0.0.1:8000/media/book_covers/book1.webp
