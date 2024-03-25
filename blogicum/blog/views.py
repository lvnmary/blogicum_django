from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Category, Post

from .constants import NUM_POSTS


def get_posts():
    return Post.objects.prefetch_related(
        'category', 'author', 'location'
    ).filter(
        pub_date__lt=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


def index(request):
    post_list = (
        get_posts()
        .order_by('-pub_date')[:NUM_POSTS]
    )
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, post_id):
    post = get_object_or_404(
        get_posts(),
        pk=post_id,
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    post_list = get_posts().filter(category=category)
    return render(
        request,
        'blog/category.html',
        {'category': category, 'post_list': post_list}
    )
