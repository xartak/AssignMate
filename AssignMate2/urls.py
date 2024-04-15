from django.urls import path, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from assign.sitemaps import HomeworkSitemap

sitemaps = {
    'homeworks': HomeworkSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('assign/', include('assign.urls', namespace='assign')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]