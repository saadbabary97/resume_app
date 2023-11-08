from django.contrib import admin
from media_file.models import Post, PostMedia, PostReaction, Comment, SharePost, UserFriends

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

class SharePostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at', 'updated_at', 'share_reaction', 'share_comment')
    search_fields = ('user__email', )

admin.site.register(Post, PostAdmin)
admin.site.register(PostMedia, PostMediaAdmin)
admin.site.register(PostReaction, PostReactionAdmin)
admin.site.register(Comment, PostCommentAdmin)
admin.site.register(SharePost, SharePostAdmin)
admin.site.register(UserFriends)
# Register your models here.
