from django.contrib import admin

from .models import Post

# This is custom admin view Post Model
class PostModelAdmin(admin.ModelAdmin):
    # In default, in admin area we see only title (what will be return __unicode__)
    # we can modify admin table and add some Model field
    list_display = ['title', 'updated', 'timestamp']

    # updated will be link
    list_display_links = ['updated']

    # add filters by fields
    list_filter = ['updated', 'timestamp']

    # add searchable field
    search_fields = ['title', 'content']

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)