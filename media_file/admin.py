from django.contrib import admin
from media_file.models import Post, PostMedia, PostReaction, Comment, SharePost

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'created_at', 'updated_at', 'user', 'is_subpost')

    search_fields = ('user__email', 'created_at')
    list_filter = ('title',)
    ordering = ()

class PostMediaAdmin(admin.ModelAdmin):
    list_display = ('post', 'video', 'image', 'stickers', 'subpost')
    ordering = ()

class PostReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'reaction_type')
    search_fields = ('user__email',)
    ordering = ()

class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment_body', 'created_at', 'updated_at')
    search_fields = ('user__email',)
    ordering = ()


admin.site.register(Post, PostAdmin)
admin.site.register(PostMedia, PostMediaAdmin)
admin.site.register(PostReaction, PostReactionAdmin)
admin.site.register(Comment, PostCommentAdmin)
admin.site.register(SharePost)
# Register your models here.
