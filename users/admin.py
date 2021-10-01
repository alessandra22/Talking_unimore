from django.contrib import admin
from .models import Profile
from blog.models import Post


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_display = ('profilo', 'n_post', 'n_interazioni_ricevute', 'avg_reputazione')

    def profilo(self, obj):
        return Profile.objects.filter(id=obj.id).first()

    def propri_post(self, obj):
        return Post.objects.filter(author=obj.user)

    def n_post(self, obj):
        return self.propri_post(obj).count()

    def n_interazioni_ricevute(self, obj):
        posts = self.propri_post(obj)
        n_ir = 0
        for post in posts:
            n_ir += post.total_likes()
            n_ir += post.total_dislikes()

        return n_ir

    def avg_reputazione(self, obj):
        posts = self.propri_post(obj)
        if self.n_post(obj) > 0:
            avg = 0
            for post in posts:
                avg += post.reputazione

            return avg/self.n_post(obj)

        else:
            return 0



