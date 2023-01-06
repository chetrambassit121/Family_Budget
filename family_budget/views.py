from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Project, Category, Expense
from django.urls import reverse 
from django.views.generic import CreateView
from .forms import ExpenseForm, ProjectForm
import json 
from django.views.generic import CreateView, DeleteView, DetailView, View, ListView
from django.core.paginator import Paginator
from django.contrib import messages
# from django.contrib.messages import messages 
from users.models import User, UserProfile
# import requests



def home(request):
    return render(request, 'budget/home.html')


class projectlist(DetailView, ListView):
    def get(self, request, pk, *args, **kwargs):
        projects = Project.objects.get(pk=pk)
        user=projects.author
        p = Paginator(Project.objects.filter(author=user), 2)
        page = request.GET.get("page")
        project_list = p.get_page(page)

        if request.method == 'DELETE':
            id = json.loads(request.body)['id']
            project = Project.objects.get(id=id)
            project.delete()
            return HttpResponse('')
        return render(request, 'budget/project_list.html', {'project_list': project_list, 'projects':projects, 'user':user})

def project_list(request):
    project_list = Project.objects.all()   
    if request.method == 'DELETE':
        id = json.loads(request.body)['id']
        project = Project.objects.get(id=id)
        project.delete()
        return HttpResponse('')
    return render(request, 'budget/project_list.html', {'project_list': project_list})





# class User_List(DetailView, ListView):
#     def get(self, request, pk, *args, **kwargs):
#         profile = UserProfile.objects.get(pk=pk)   
#         user = profile.user

#         context = {
#             # 'projects':projects,
#             'user':user,
#             # 'profile':profile
#         }
#         return render(request, 'budget/user_list.html', {'users':users})

         




# class ProfilePageView(DetailView, ListView):
#     def get(self, request, pk, *args, **kwargs):
#         profile = UserProfile.objects.get(pk=pk)
#         user = profile.user
#         p = Paginator(Project.objects.filter(author=user), 1)
#         page = request.GET.get("page")
#         projects = p.get_page(page)

#         context = {
#             'projects':projects,
#             'user':user,
#             'profile':profile
#         }

#         return render(request, "registration/profile_page.html", context)




def project_detail(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    if request.method == 'GET':
        category_list = Category.objects.filter(project=project)
        return render(request, 'budget/project_detail.html', {'project': project, 'expense_list': project.expenses.all(), 'category_list': category_list})

    elif request.method == 'POST':
        # process the form
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']

            category = get_object_or_404(Category, project=project, name=category_name)

            Expense.objects.create(
                project=project,
                title=title,
                amount=amount,
                category=category
            ).save()

    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = Expense.objects.get(id=id)
        expense.delete()

        return HttpResponse('')

    return HttpResponseRedirect(project_slug)


# class ProjectCreateView(CreateView):
#     model = Project
#     template_name = 'budget/project_add.html'
#     fields = ('name', 'budget')

#     def form_valid(self, form, request):
#         self.object = form.save(commit=False)
#         self.author = request.user
#         self.object.save(request)
#         categories = self.request.POST['categoriesString'].split(',')

#         for category in categories:
#             Category.objects.create(
#                 project=Project.objects.get(id=self.object.id),
#                 name=category
#             ).save()
#         return HttpResponseRedirect('/' + self.get_success_url())


#     def get_success_url(self):
#         return slugify(self.request.POST['name'])


class ProjectCreateView(CreateView):
    # model = Project
    def get(self, request, *args, **kwargs):
        form = ProjectForm()
        context = {
            "form": form,
        }

        return render(request, "budget/project_add.html", context)
        
    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.author = request.user
            new_project.save(request)
            categories = self.request.POST['categoriesString'].split(',')
            for category in categories:
                Category.objects.create(
                    project=Project.objects.get(id=new_project.id),
                    name=category
                ).save()
            form = ProjectForm()
            messages.success(request, "Budget successfully created! Add another!")

        # projects = Project.objects.all()
        # profile = UserProfile.objects.get(pk=pk)
        # user = profile.user
        # p = Paginator(Project.objects.filter(author=user), 2)
        # page = request.GET.get("page")
        # projects = p.get_page(page)

        # context = {
        #     'projects':projects,
        #     'user':user,
        #     'profile':profile
        # }
            
        #     return HttpResponseRedirect('/' + self.get_success_url())

        # def get_success_url(self):
        #     return slugify(self.request.POST['name'])
        # return render(request, "registration/profile_page.html", context)
        return render(request, "budget/project_add.html", {'form':form})