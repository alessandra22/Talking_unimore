from django.contrib import admin
from .models import Post, Comment, Thread, Type
from users.models import Profile


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['content']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'n_commenti')
    search_fields = ['title', 'content']

    def n_commenti(self, obj):
        return Post.objects.filter(id=obj.id).first().post_comment.count()


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    search_fields = ['thread']
    list_display = ('thread', 'periodo', 'n_post', 'n_follower')

    def n_post(self, obj):
        return Post.objects.filter(thread=obj).count()

    def n_follower(self, obj):
        return Profile.objects.filter(threads=obj).count()


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'n_post')
    search_fields = ['type']

    def n_post(self, obj):
        return Post.objects.filter(type=obj).count()
