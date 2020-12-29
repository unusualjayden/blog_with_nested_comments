from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    CreateView,
    DeleteView,
    UpdateView
)

from .forms import (
    RegistrationForm,
    PostForm,
    CommentForm
)
from .models import (
    Post,
    Comment
)


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'post_list.html'


def detail_post_view(request, post):
    post = get_object_or_404(Post, slug=post, status='published')

    all_comments = Comment.objects.filter(post=post).get_descendants(include_self=True)

    user_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.author = request.user
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect(reverse('posts:post-detail', args=[post.slug]))
    else:
        comment_form = CommentForm()
    return render(request, 'post_detail.html', {
        'post': post,
        'slug': post.slug,
        'comments': user_comment,
        'comment_form': comment_form,
        'all_comments': all_comments,
    })


class RegistrationView(FormView):
    template_name = 'signup.html'
    form_class = RegistrationForm
    success_url = '/'

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(
            form.cleaned_data['password'])
        form.save()
        return super(RegistrationView, self).form_valid(form)


class ProfileView(DetailView):
    model = User
    template_name = 'user_profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_current_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['published_posts'] = Post.published.filter(author=self.get_current_user())
        context['draft_posts'] = Post.draft.filter(author=self.get_current_user())
        context['current_profile'] = self.request.user
        return context


class NewPostView(CreateView):
    model = Post
    template_name = 'new_post.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NewPostView, self).form_valid(form)


class DeletePostView(DeleteView):
    model = Post

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])

    def get_object(self, queryset=None):
        obj = super(DeletePostView, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        return obj


class UpdatePostView(UpdateView):
    model = Post
    fields = ('title', 'body', 'slug')
    template_name = 'comment_update.html'

    def get_success_url(self):
        return reverse('profile', args=[self.object.get_root().post.slug])

    def get_context_data(self, **kwargs):
        context = super(UpdatePostView, self).get_context_data(**kwargs)
        context['comment_author'] = self.object.author
        return context


def comment_reply_view(request, post, pk):
    comment = Comment.objects.get(id=pk)
    post = Post.objects.get(slug=post)

    user_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.author = request.user
            user_comment.parent = comment
            user_comment.save()
            return HttpResponseRedirect(reverse('posts:post-detail', args=[post.slug]))
    else:
        comment_form = CommentForm()
    return render(request, 'comment_reply.html', {
        'comment': comment,
        'slug': post.slug,
        'comments': user_comment,
        'comment_form': comment_form,
    })


class DeleteCommentView(DeleteView):
    model = Comment

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        if self.object.post:
            return reverse('posts:post-detail', args=[self.object.post.slug])
        else:
            root = self.object.parent.get_root()
            return reverse('posts:post-detail', args=[root.post.slug])

    def get_object(self, queryset=None):
        obj = super(DeleteCommentView, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        return obj


class UpdateCommentView(UpdateView):
    model = Comment
    fields = ('content',)
    template_name = 'comment_update.html'

    def get_success_url(self):
        return reverse('posts:post-detail', args=[self.object.get_root().post.slug])

    def get_context_data(self, **kwargs):
        context = super(UpdateCommentView, self).get_context_data(**kwargs)
        context['comment_author'] = self.object.author
        return context
