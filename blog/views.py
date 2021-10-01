from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, Thread, Type
from .forms import MyPostForm, MyCommentForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


class PostListView(ListView):
    model = Post
    template_name = 'blog/main_home.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = '-date_posted'


class OrderedPostListView(ListView):
    model = Post
    template_name = 'blog/main_home.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        if self.kwargs.get('order') == '-reputazione':
            return Post.objects.all().order_by('-reputazione', '-date_posted')
        else:
            return Post.objects.all().order_by('-date_posted')


@method_decorator(login_required, name='dispatch')
class MyPostListView(ListView):
    model = Post
    template_name = 'blog/my_home.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user == get_object_or_404(User, username=self.kwargs.get('username')):
            threads = list()

            for thread in self.request.user.user_profile.threads.all():
                threads.append(thread)

            posts = Post.objects.filter(type=-2)  # non esiste
            for thread in threads:
                # posts |= Post.objects.annotate(nome_thread='thread.nome').filter(nome_thread=nome)
                posts |= Post.objects.filter(thread=thread)

            if self.kwargs.get('order') == '-reputazione':
                return posts.order_by('-reputazione', '-date_posted')
            else:
                return posts.order_by('-date_posted')

        raise PermissionDenied({"message": "Non puoi accedere alla home di un altro utente!"})


class ThreadPostListView(ListView):
    model = Post
    template_name = 'blog/thread_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        mythread = Thread.objects.filter(thread=self.kwargs.get('thread')).first().id
        if self.kwargs.get('order') == '-reputazione':
            return Post.objects.filter(thread=mythread).order_by('-reputazione', '-date_posted')
        else:
            return Post.objects.filter(thread=mythread).order_by('-date_posted')


class TypePostListView(ListView):
    model = Post
    template_name = 'blog/type_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        mytype = Type.objects.filter(type=self.kwargs.get('type')).first().id
        if self.kwargs.get('order') == '-reputazione':
            return Post.objects.filter(type=mytype).order_by('-reputazione', '-date_posted')
        else:
            return Post.objects.filter(type=mytype).order_by('-date_posted')


class ThreadTypePostListView(ListView):
    model = Post
    template_name = 'blog/thread_type_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        mytype = Type.objects.filter(type=self.kwargs.get('type')).first().id
        mythread = Thread.objects.filter(thread=self.kwargs.get('thread')).first().id
        post_filtrati = Post.objects.filter(type=mytype).filter(thread=mythread)
        if self.kwargs.get('order') == '-reputazione':
            return post_filtrati.order_by('-reputazione', '-date_posted')
        else:
            return post_filtrati.order_by('-date_posted')


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))

        if self.kwargs.get('order') == '-reputazione':
            return Post.objects.filter(author=user).order_by('-reputazione', '-date_posted')
        else:
            return Post.objects.filter(author=user).order_by('-date_posted')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = MyPostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'type', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()

        user = get_object_or_404(Post, id=self.kwargs['pk'])
        n_like = user.total_likes()
        n_dislike = user.total_dislikes()

        liked = False
        disliked = False

        if user.like.filter(id=self.request.user.id).exists():
            liked = True

        if user.dislike.filter(id=self.request.user.id).exists():
            disliked = True

        context["n_like"] = n_like
        context["liked"] = liked
        context["n_dislike"] = n_dislike
        context["disliked"] = disliked

        return context


def like_view(request, post_id):
    post = get_object_or_404(Post.objects.filter(id=post_id))
    if post.like.all().filter(id=request.user.id).exists():
        post.like.remove(request.user)
        post.reputazione -= 1
    else:
        post.like.add(request.user)
        post.reputazione += 1

    if post.dislike.all().filter(id=request.user.id).exists():
        post.dislike.remove(request.user)
        post.reputazione += 1

    post.save()
    return HttpResponseRedirect(reverse('post-detail', args=[str(post_id)]))


def dislike_view(request, post_id):
    post = get_object_or_404(Post.objects.filter(id=post_id))
    if post.dislike.all().filter(id=request.user.id).exists():
        post.dislike.remove(request.user)
        post.reputazione += 1
    else:
        post.dislike.add(request.user)
        post.reputazione -= 1

    if post.like.all().filter(id=request.user.id).exists():
        post.like.remove(request.user)
        post.reputazione -= 1

    post.save()
    return HttpResponseRedirect(reverse('post-detail', args=[str(post_id)]))


def list_esami_view(request, periodo):
    threads = Thread.objects.filter(periodo=periodo)
    list_esami = list()
    for thread in threads:
        list_esami.append(thread.thread)

    return render(request, 'blog/list.html', {'list_esami': list_esami})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = MyCommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.all().filter(id=self.kwargs.get('pk')).first()
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        comment = Comment.objects.all().filter(id=self.kwargs.get('pk')).first()
        form.instance.post = comment.post
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        postid = self.kwargs.get('pkp')
        return f"/post/{postid}"

    def test_func(self):
        comment = Comment.objects.all().filter(pk=self.kwargs.get('pk')).first()
        print(comment)
        if self.request.user == comment.author:
            return True
        return False


class LikedPostListView(ListView):
    model = Post
    template_name = 'blog/liked_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        if self.kwargs.get('order') == '-reputazione':
            return Post.objects.filter(like=self.request.user).order_by('-reputazione', '-date_posted')
        else:
            return Post.objects.filter(like=self.request.user).order_by('-date_posted')
