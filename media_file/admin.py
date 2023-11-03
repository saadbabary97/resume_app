from django.contrib import admin
from media_file.models import Post, PostMedia, PostReaction, Comment

admin.site.register(Post)
admin.site.register(PostMedia)
admin.site.register(PostReaction)
admin.site.register(Comment)
# Register your models here.
