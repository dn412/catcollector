from django.urls import path
from . import views
# this file is how we're going to map our urls to views
# remember in django, views are like our controllers
# the `name='home'` is a kwarg, that gives the route a name. naming routes is optional, but best practices
# later on, we'll see just how useful this is.
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # route for cats index
    path('cats/', views.cats_index, name='index'),
    # route for the cats detail
    path('cats/<int:cat_id>', views.cats_detail, name='detail'),
    path('cats/create/', views.CatCreate.as_view(), name='cats_create'),
    path('cats/<int:pk>/update/', views.CatUpdate.as_view(), name='cats_update'),
    path('cats/<int:pk>/delete/', views.CatDelete.as_view(), name='cats_delete'),
    path('cats/<int:cat_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    # url for s3 upload
    path('cats/<int:cat_id>/add_photo', views.add_photo, name='add_photo'),
    # we need several urls for our Toys to work
    # we'll need a list, detail, create, update, delete
    path('toys/', views.ToyList.as_view(), name='toys_index'),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
    # eventually, once it's all set up, we'll add two views to handle the relationship between a cat and a toy.
    path('cats/<int:cat_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    path('cats/<int:cat_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),
]