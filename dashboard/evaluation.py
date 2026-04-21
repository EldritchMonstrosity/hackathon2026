from django.shortcuts import render, redirect, get_object_or_404
from .models import Post

def compute_eval(request):

    liked_ids = request.session.get("liked_posts", [])
    liked_posts = Post.objects.filter(id__in=liked_ids)

    disliked_ids = request.session.get("disliked_posts", [])
    disliked_posts = Post.objects.filter(id__in=disliked_ids)

    final_eval = {
        "meme": 0,
        "sports": 0,
        "science": 0,
        "politics": 0,
        "art": 0,
        "pop_culture": 0,
    }

    # boost liked posts
    for post in liked_posts:
        for keY, value in post.post_eval_dict.items():
            final_eval[keY] += value

    # penalize disliked posts
    for post in disliked_posts:
        for keY, value in post.post_eval_dict.items():
            final_eval[keY] -= value
    
    # averaging it all
    for keY in final_eval:
        final_eval[keY] /= (len(disliked_posts)+len(liked_posts))

    return final_eval