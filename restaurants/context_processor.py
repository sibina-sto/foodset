from django.shortcuts import get_object_or_404
from restaurants.models import Restaurant

def categories(request):
    # Using values_list and set for distinct categories
    categories_set = set(Restaurant.objects.values_list('categories', flat=True))
    return {'categories_set': categories_set}

def user_liked_posts(request):
    if request.user.is_authenticated:
        liked_posts = Restaurant.objects.filter(likes=request.user.id)
        return {'user_liked_posts': liked_posts}
    else:
        # Return an empty queryset for consistency
        return {'user_liked_posts': Restaurant.objects.none()}

def recent_posts(request):
    recent_posts = Restaurant.objects.all().order_by('-created_at')[:10]
    return {'recent_posts': recent_posts}
