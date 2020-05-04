from django.shortcuts import render , get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView
from django.contrib.auth.models import User
from .models import Post
from django.http import HttpResponse, HttpResponseRedirect


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def post_detail(request , id):
    post = get_object_or_404(Post , id = id)
    is_liked = False
    if post.likes.filter(id = request.user.id).exists():
        is_liked = True
    context = {
        'post' : post,
        'is_liked' : is_liked,
        'total_likes' : post.total_likes(),
    }
    # return render(request , 'blog/post_detail.html' , context)

def like_post(request):

    post = get_object_or_404(Post , id = request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<view_type>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html' #<app>/<model>_<view_type>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User , username = self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post



class PostCreateView(LoginRequiredMixin , CreateView):
    model = Post
    fields = ['title' , 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin , UserPassesTestMixin ,  UpdateView):
    model = Post
    fields = ['title' , 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin , UserPassesTestMixin , DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False




def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})