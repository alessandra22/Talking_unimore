from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Thread(models.Model):
    thread = models.CharField(max_length=100)
    periodo = models.CharField(choices={
        ('Primo anno', 'Primo anno'),
        ('Secondo anno', 'Secondo anno'),
        ('Terzo anno', 'Terzo anno'),
        ('Facoltativi', 'Facoltativi')
    }, max_length=100, default='Primo anno')

    def __str__(self):
        return self.thread


class Type(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='pics')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='post_type')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='post_thread')

    like = models.ManyToManyField(User, related_name='post_like')
    dislike = models.ManyToManyField(User, related_name='post_dislike')
    reputazione = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.karma2 = 0

    def total_likes(self):
        return self.like.count()

    def total_dislikes(self):
        return self.dislike.count()

    def interazioni(self):
        return self.total_likes() + self.total_dislikes()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self):
        super().save()

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Commento di {self.author} al post {self.post.title}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.id})
