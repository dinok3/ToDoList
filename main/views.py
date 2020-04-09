from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404
from .models import todolist,items
from .filters import todolistFilter
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  DeleteView,UpdateView)
from django.contrib.auth.models import User
# Create your views here.





class TodoListView(ListView):
    filterset_class = todolistFilter
    model = todolist
    context_object_name = "todos"
    ordering = ["-date_created"]
    template_name = "main/main.html"
    paginate_by = 3

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        queryset = super().get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context



def detail(request,id):
    todos = todolist.objects.get(id=id)

    t = todolist.objects.all()



    if request.method == "POST":
        if request.POST.get("save"):
            for item in todos.items_set.all():
                if request.POST.get("c" + str(item.id)) == "clicked":
                    item.checked = True
                else:
                    item.checked = False
                item.save()

        elif request.POST.get("newitem"):
            txt = request.POST.get("new")

            if len(txt)>1:
                todos.items_set.create(item_name=txt,checked=False)
            else:
                print("Invalid!")



    return render(request,"main/todolist_detail.html",{"todos":todos,"t":t})



def items(request,id,pk):
    todos = todolist.objects.get(id=id)
    items = todos.items_set.get(pk=pk)


    if request.method == "POST":
        if request.user == todos.author:

            if request.POST.get("delete"):
                print(request.user)
                print(todos.author)
                items.delete()
                todos.save()
                return redirect("/")

            elif request.POST.get("update"):
                return redirect("update/")
        else:
            raise Http404("You are not allowed to make changes for others!")


    return render(request,"main/items.html",{"todos":todos,"items":items})







class TodoDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = todolist
    success_url = "/"

    def test_func(self):
        t = self.get_object()
        if self.request.user == t.author:
            return True

        return False






class TodoCreateView(LoginRequiredMixin, CreateView):
    model = todolist
    fields = ["name"]
    success_url = "/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)







class TodoUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = todolist
    fields = ["name"]

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        t = self.get_object()
        if self.request.user == t.author:
            return True
        return False



class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = items
    fields = ["item_name"]

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)





