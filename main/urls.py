from . import views
from django.urls import path,include
from .views import TodoCreateView,TodoDeleteView,TodoUpdateView,ItemUpdateView,TodoListView
#ItemDeleteView
from .models import *

urlpatterns = [

    #path("",views.home,name="home-page"),
    path("",TodoListView.as_view(),name="home-page"),

    path("todolist/<int:id>/",views.detail,name="todolist-detail"),
    path("todolist/<int:pk>/update/",TodoUpdateView.as_view(),name="todolist-update"),
    path("todolist/<int:id>/item/<int:pk>/update/",ItemUpdateView.as_view(model=items),name="item-update"),
    path("todolist/new/",TodoCreateView.as_view(),name="todolist-create"),
    path("todolist/<int:id>/item/<int:pk>/",views.items,name="items"),
    path("todolist/<int:pk>/delete/",TodoDeleteView.as_view(),name="todolist-delete")
]

#app/model_viewtypes.html