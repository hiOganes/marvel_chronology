from django.contrib.sitemaps import Sitemap
from apps.movies.models import Movies


class MoviesSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Movies.objects.all()

    def lastmod(self, obj):
        return obj.updated_at