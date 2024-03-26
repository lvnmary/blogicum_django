from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from blog.forms import PostForm
from blog.models import Comment, Post


class PostMixin(LoginRequiredMixin):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(self.model, pk=kwargs[self.pk_url_kwarg])
        if instance.author != request.user:
            return redirect('blog:post_detail', kwargs[self.pk_url_kwarg])
        return super().dispatch(request, *args, **kwargs)


class CommentMixin(LoginRequiredMixin):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(self.model, pk=kwargs[self.pk_url_kwarg])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            args=(self.kwargs['post_id'],)
        )


class PublishedPostsMixin:
    def get_published_posts(self, model):
        return model.objects.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )


class AnnotateCommentMixin:
    def annotate_comment_count(self, queryset=Post.objects):
        return queryset.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
