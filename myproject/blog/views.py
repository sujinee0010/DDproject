from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from blog.models import Post


#글 목록 조회
def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-created_date')  # 수정된 부분
    context ={
        'posts':posts,
    }
    #세번째 인자 딕셔너리 타입
    return render(request, 'blog/post_list.html',context)

def post_detail(request ,pk ):
    post = Post.objects.get(pk=pk)
    context = {
        'post':post
    }
    return render(request,'blog/post_detail.html',context)

def post_add(request):
    if request.method == 'POST':
        User = get_user_model()
        author = User.objects.get(username ='zzzng')
        title = request.POST['title']
        content = request.POST['content']
        post = Post.objects.create(
            author=author,
            title=title,
            content=content,
        )
        post.publish()

        post_pk= post.pk
        #redirect(뷰이름, 매개변수명=인자)
        return redirect(post_detail, pk=post_pk)
    elif request.method == 'GET':
        return render(request, 'blog/post_add.html')

def post_delete(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.delete()
        return render(request, 'blog/post_delete.html')

    elif request.method == 'GET':
        return HttpResponse('잘못된 접근 입니다.')