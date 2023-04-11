from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator


def home(request):
    blogs = Blog.objects.all()
    blogs_number = []
    blogs_len = int((len(blogs)+1)/2)
    for i in range(1, blogs_len):
        blogs_number.append(i)
    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'home.html',{'page_obj':page_obj,'blogs_number':blogs_number, 'blogs_len': blogs_len})


def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request,'detail.html',{'blog':blog})


def new(request):
    return render(request,'new.html')


def create(request):
    new_blog = Blog()
    new_blog.title = request.POST.get('title')
    new_blog.content = request.POST.get('content')
    new_blog.image = request.FILES.get('image')
    new_blog.save()
    return redirect('detail', new_blog.id)


def edit(request, blog_id):
    edit_blog = get_object_or_404(Blog, pk=blog_id) # print() 해보기
    return render(request, 'edit.html', {'edit_blog':edit_blog})


def update(request, blog_id):
    old_blog = get_object_or_404(Blog, pk=blog_id)
    old_blog.title = request.POST.get('title')
    old_blog.content = request.POST.get('content')
    old_blog.image = request.FILES.get('image')
    old_blog.save()
    return redirect('detail', old_blog.id)

def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    delete_blog.delete()
    return redirect('home')


def search(request):
    if request.method == 'POST':
        searched = request.POST['Search'] #검색어
        choice = request.POST['choice'] #검색범위

        #검색 범위 안에서만 검색할 수 있도록 필터지정
        if(choice == '제목'):
            keyword = Blog.objects.filter(Q(title__icontains=searched)).distinct()
        elif(choice == '본문'):
            keyword = Blog.objects.filter(Q(content__icontains=searched)).distinct()
        else:
            keyword = Blog.objects.filter(Q(title__icontains=searched) | Q(content__icontains=searched)).distinct()

        return render(request, 'searched.html', {'searched': searched, 'keywords': keyword, 'choice':choice})
    else:
        return render(request, 'searched.html')