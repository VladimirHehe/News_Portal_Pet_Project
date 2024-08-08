from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from news.models import Post, Author


@login_required
def UserProfile(request):
    user_post = Post.objects.filter(author=Author.objects.get(user=request.user))
    author = Author.objects.get(user=request.user)
    if request.method == 'GET':
        author.update_rating()
        author.save()
        return render(request, 'account/profile.html', {'user_post': user_post, 'author': author})
    return render(request, 'account/profile.html', {'user_post': user_post})


def exit_to_profile(request):
    if request.method == 'GET':
        return redirect('accounts/logout')



