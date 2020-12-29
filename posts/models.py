from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class PublishedManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class DraftManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='draft')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish', blank=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    objects = models.Manager()
    published = PublishedManger()
    draft = DraftManger()

    class Meta:
        ordering = ('-publish', 'title')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post-detail', args=[self.slug])

    def get_delete_url(self):
        return reverse('posts:post-delete', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_str = self.title
            if Post.objects.filter(slug=slugify(slug_str)):
                slug_str = slug_str + ' ' + f'{self.id}'
            self.slug = slugify(slug_str)
        super(Post, self).save(*args, **kwargs)


class Comment(MPTTModel):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comment_author', null=True)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments', null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['publish']


    def __str__(self):
        return self.content
