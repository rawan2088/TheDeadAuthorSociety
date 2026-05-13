from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include('authentication.urls')),
    # path('api/books/', include('All.urls')),
    # path('api/', include('authentication.urls')),
    path("api/",    include("All.urls")),  
]
# This makes Django serve files at http://127.0.0.1:8000/media/book_covers/book1.webp.

# in django we use this path
# book_covers/book1.webp
#  request.build_absolute_uri(book.image.url) turns it into:
# http://127.0.0.1:8000/media/book_covers/book1.webp
