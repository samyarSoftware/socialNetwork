from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import User, Post, TicketReply
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, "social/home.html")


def profile(request):
    return render(request, "social/profile.html")


def user_login(request):
    user = get_object_or_404(User, username=request.user.username)
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                 password=form.cleaned_data['password'])
            login(request, user)
            return redirect("social:profile")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {'form': form})
        

def user_logout(request):
    logout(request)
    return HttpResponse("شما خارج شدید")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect("social:profile")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {'form': form})


@login_required(login_url='/social/login')
def user_edit(request):
    user = get_object_or_404(User, id=request.user.id)
    if request.method == "POST":
        form = UserEdit(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("social:profile")
    else:
        form = UserEdit(instance=user)
    return render(request, "registration/user-edit.html", {'form': form})


# @login_required
def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            massage = f"{cd['name']}\n{cd['phone']}\n{cd['massage']}"

            if user.is_superuser:
                send_mail(cd['subject'], massage, user.email, ['samiramoosazadeh65@gmail.com'], fail_silently=False)

            send_mail(cd['subject'], massage, user.email, ['samyartavakkoli87@gmail.com'], fail_silently=False)

            messages.success(request, "تیکت شما ارسال شد")
            form.save()
    else:
        form = TicketForm()
    return render(request, "forms/ticket.html", {'form': form})


# @login_required
def password_change(request):
    if request.method == "POST":
        form = CustomPassChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "registration/password-change-done.html")
    else:
        form = CustomPassChangeForm()
    return render(request, "registration/password-change.html", {'form': form})


def post_list(request, tag_slug=None):
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag])
    else:
        posts = Post.objects.filter(active=True)
        tag = None
    
    page = request.GET.get('page')
    paginator = Paginator(posts, 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = []

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'social/list-ajax.html', {'posts': posts})

    context = {'posts': posts, 'tag': tag}
    return render(request, "social/posts-list.html", context)


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.author = request.user
            form.save()
            form.save_m2m()
            return redirect("social:post_list")
    else:
        form = PostForm()
    return render(request, "forms/create-post.html", {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    post_tags_id = post.tags.values_list('id', flat=True)
    similar_post = Post.objects.exclude(id=post.id).filter(tags__in=post_tags_id)
    similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('same_tags', '-created')
    context = {
        'post': post,
        'similar_post': similar_post
    }
    return render(request, "social/post-detail.html", context)


def search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.filter(Q(description__icontains=query))
    
    context = {
        'query': query,
        'results': results
    }
    return render(request, "social/search.html", context)


@login_required
def comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=post)
    if request.method == "POST":
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect("social:post_list")
    else:
        form = CommentForm()
    context = {'form': form, 'comments': comments}
    return render(request, "forms/comments.html", context)


@login_required(login_url='social:login')
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('social:profile')


@login_required(login_url='social:login')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("social:profile")
    else:
        form = PostForm(instance=post)
    return render(request, "form/edit-post.html", {'form':form, 'post': post})


@login_required(login_url='social:login')
@require_POST
def like_post(request):
    data = json.loads(request.body)
    post_id = data.get("post_id")
    try:
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        likes_count = post.likes.count()

        response_data = {'liked': liked, 'likes_count': likes_count}
    except:
        response_data = {'error': 'you got error'}
    return JsonResponse(response_data)


@login_required(login_url='social:login')
@require_POST
def save_post(request):
    data = json.loads(request.body)
    post_id = data.get("post_id")
    if post_id is not None:
        post = Post.objects.get(pk=post_id)
        if request.user in post.saved_by.all():
            post.saved_by.remove(request.user)
            saved = False
        else:
            post.saved_by.add(request.user)
            saved = True
        response_data = {'saved': saved}
    else:
        response_data = {'error': 'post id is Invalid!'}

    return JsonResponse(response_data)


def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    followers_sum = user.followers.prefetch_related().all()
    following_sum = user.following.prefetch_related().all()
    context = {
        'user': user, 'followers_sum': followers_sum, 'following_sum': following_sum
        }
    return render(request, "social/user_detail.html", context)


@login_required
@require_POST
def follow(request):
    data = json.loads(request.body)
    user_id = data.get("user_id")

    if user_id is not None:
        try:
            user = User.objects.get(id=user_id)
            if request.user in user.followers.all():
                user.followers.remove(request.user)
                follow = False
                
            else:
                user.followers.add(request.user)
                follow = True

            total_followers = user.followers.count()
            total_following = user.following.count()

            return JsonResponse({'follow': follow, 'total_followers': total_followers, 'total_following': total_following})
        except:
            return JsonResponse({'error': 'user does not exist!'})
    return JsonResponse({'error': 'user does not exist!'})


def ticket_detail(request, pk):
    try:
        ticket = Ticket.objects.select_related('user').get(user__username=request.user, id=pk) if not request.user.is_superuser else Ticket.objects.get(id=pk)
        reply_form = TicketReplyForm()
        replys = TicketReply.objects.select_related("ticket").filter(ticket=ticket)
        return render(request, "social/ticket-detail.html", {'ticket': ticket, 'reply_form': reply_form, 'replys': replys})
    except Ticket.DoesNotExist:
        raise Http404('error 404')


@require_POST
def ticket_reply(request, id):
    data = json.loads(request.body)
    ticket = get_object_or_404(Ticket, id=id)
    print(ticket)
    text = data['reply']
    form = TicketReplyForm({'text':text})
    if form.is_valid():
        reply = form.save(commit=False)
        reply.ticket = ticket
        reply.save()
        return render(request, "forms/ticket-reply.html", {'reply': reply})