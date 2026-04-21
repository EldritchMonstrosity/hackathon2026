from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post

def dashboard(request):
    return render(request, "dashboard/dashboard.html")

def post_list(request):
    posts = Post.objects.all()
    return render(request, "dashboard/post_list.html", {"posts": posts})

def post_individual(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "dashboard/post_individual.html", {"post": post})

def like_post(request, post_id):
    liked = request.session.get("liked_posts", [])

    if post_id not in liked:
        liked.append(post_id)

    request.session["liked_posts"] = liked  

    request.session.modified = True  

    return redirect("dashboard:post_individual", post_id=post_id)

def dislike_post(request, post_id):
    disliked = request.session.get("liked_posts", [])

    if post_id not in disliked:
        disliked.append(post_id)

    request.session["disliked_posts"] = disliked  

    request.session.modified = True  

    return redirect("dashboard:post_individual", post_id=post_id)


def build_dashboard_data(request):
    liked_ids = request.session.get("liked_posts", [])
    disliked_ids = request.session.get("disliked_posts", [])

    liked_posts = Post.objects.filter(id__in=liked_ids)
    disliked_posts = Post.objects.filter(id__in=disliked_ids)

    final_eval = {"politics": 0,
        "art": 0,
        "meme": 0,
        "pop_culture": 0,
        "science": 0,
        "sports": 0,

        "christian": 0,
        "islam": 0,
        "hinduism": 0,
    }

    def accumulate(posts, weight):
        for post in posts:
            for k, v in post.post_eval_dict.items():
                final_eval[k] = final_eval.get(k, 0) + (v * weight)

    accumulate(liked_posts, +1)
    accumulate(disliked_posts, -1)
    
    def average():
        for k in final_eval:
            final_eval[k] /= (len(liked_posts)+len(disliked_posts))

    average()

    return {
        "final_eval": final_eval,
        "liked_posts": liked_posts,
        "disliked_posts": disliked_posts,
    }

def dashboard(request):
    data = build_dashboard_data(request)

    return render(request, "dashboard/dashboard.html", data)

def category_analysis(request, category):
    liked_ids = request.session.get("liked_posts", [])
    disliked_ids = request.session.get("disliked_posts", [])

    liked_posts = Post.objects.filter(id__in=liked_ids)
    disliked_posts = Post.objects.filter(id__in=disliked_ids)

    def filter_by_category(posts):
        return [
            post for post in posts
            if post.post_eval_dict.get(category, 0) != 0
        ]

    context = {
        "category": category,
        "liked_posts": filter_by_category(liked_posts),
        "disliked_posts": filter_by_category(disliked_posts),
    }

    return render(request, "dashboard/category_analysis.html", context)