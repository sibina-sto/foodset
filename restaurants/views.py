from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import RestaurantCreateForm
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Restaurant, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseBadRequest


class RestaurantListView(ListView):
    queryset = Restaurant.objects.all()
    paginate_by = 6
    template_name = 'restaurants/restaurant_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        cat = self.request.GET.get('cat')
        author = self.request.GET.get('author')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(details__icontains=q)
            ).distinct()

        if cat:
            queryset = queryset.filter(categories__icontains=cat)

        if author:
            queryset = queryset.filter(user__username=author)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Restaurant.objects.values_list('categories', flat=True).distinct()
        return context

    @staticmethod
    def handle_post_like_unlike(request, post_id, unlike=True):
        if post_id:
            post = get_object_or_404(Restaurant, id=post_id)
            if unlike:
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.method == 'POST':
            post_id = request.POST.get('unlike')
            post_id2 = request.POST.get('like')
            self.handle_post_like_unlike(request, post_id)
            self.handle_post_like_unlike(request, post_id2, unlike=False)
            return redirect('home')
        return HttpResponseBadRequest("Invalid request")


class RestaurantDetailView(DetailView):
    queryset = Restaurant.objects.all()

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        comment = request.POST.get('comment')
        c_slug = request.POST.get('slug')

        if comment is not None and c_slug is not None:
            post = get_object_or_404(Restaurant, slug=c_slug)
            comment = Comment.objects.create(
                user=request.user, post=post, text=comment
            )
            comment.save()

        return redirect('detail', c_slug)


class RestaurantCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'restaurants/restaurant_form.html'
    form_class = RestaurantCreateForm
    success_url = reverse_lazy('my_posts')
    success_message = "Post Created Successfully"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)


class RestaurantUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = RestaurantCreateForm
    template_name = 'restaurants/restaurant_form.html'
    success_url = reverse_lazy('my_posts')
    success_message = "Post Updated Successfully"

    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)


class RestaurantDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy('my_posts')
    success_message = "Post Deleted Successfully"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)


class MyPostView(LoginRequiredMixin, ListView):
    template_name = 'restaurants/my_posts.html'
    ordering = ['-created_at']  # Add this line to order by creation date

    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)