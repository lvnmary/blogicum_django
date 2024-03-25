from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)

from blog.forms import PostForm, CommentForm
from blog.models import Category, Post, User
from blog.mixins import (PostMixin, CommentMixin,
                         PublishedPostsMixin, AnnotateCommentMixin)
from blog.constants import POSTS_PER_PAGE


class PostView(PublishedPostsMixin, AnnotateCommentMixin, ListView):
    paginate_by = POSTS_PER_PAGE
    template_name = 'blog/index.html'

    def get_queryset(self):
        posts = self.get_published_posts(Post)
        return (
            self.annotate_comment_count(posts)
            .select_related('author', 'category', 'location')
        )


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            args=(self.request.user.username,)
        )


class DetailPostView(DetailView):
    model = Post
    form_class = CommentForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['comments'] = self.object.comments.all()
        return context

    def get_object(self, queryset=None):
        post = super().get_object()
        if post.author == self.request.user or post.is_published:
            return post
        raise Http404


class EditPostView(PostMixin, UpdateView):

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', args=(self.kwargs['post_id'],)
        )


class DeletePostView(PostMixin, DeleteView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context

    def get_success_url(self):
        return reverse(
            'blog:profile', args=(self.request.user.username,)
        )


class CategoryView(PublishedPostsMixin, AnnotateCommentMixin, ListView):
    paginate_by = POSTS_PER_PAGE
    template_name = 'blog/category.html'

    def get_queryset(self):
        posts = self.get_published_posts(Post).filter(
            category__slug=self.kwargs['category_slug']
        )
        return (
            self.annotate_comment_count(posts)
            .select_related('author', 'category', 'location')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category.objects.filter(is_published=True),
            slug=self.kwargs['category_slug']
        )
        return context


class ProfileView(PublishedPostsMixin, AnnotateCommentMixin, ListView):
    paginate_by = POSTS_PER_PAGE
    template_name = 'blog/profile.html'

    def get_queryset(self):
        username = self.kwargs.get('username')
        if self.request.user.username == username:
            return (
                self.annotate_comment_count()
                .filter(author__username=username)
                .select_related('author', 'category', 'location')
                .order_by('-pub_date')
            )

        posts = self.get_published_posts(Post).filter(author__username=username)
        return (
            self.annotate_comment_count(posts)
            .select_related('author', 'category', 'location')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile', args=(self.request.user.username,)
        )


class CreateCommentView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', args=(self.kwargs['post_id'],)
        )


class EditCommentView(CommentMixin, UpdateView):
    form_class = CommentForm


class DeleteCommentView(CommentMixin, DeleteView):
    pass
