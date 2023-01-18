from django.urls import path, include
from .views import project_detail, project_list, projectlist, ProjectCreateView, ProjectCreateView, home
from . import views 


urlpatterns = [
    path('', home, name='home'),
    # path('project_list/', projectlist.as_view(), name='list'),
    path('project_list/', project_list, name='list'),
    path('add/', ProjectCreateView.as_view(), name='add'),
    # path('add/', ProjectCreateView, name='add'),
    path('<slug:project_slug>', project_detail, name='detail'),
    # path("user_list/", User_List.as_view(), name="user_list"),
]



# urlpatterns = [
#     path('', home, name='home'),
#     # path('project_list/', projectlist.as_view(), name='list'),
#     path('project_list/', project_list, name='list'),
#     path('add/', ProjectCreateView.as_view(), name='add'),
#     # path('add/', ProjectCreateView, name='add'),
#     path('<slug:project_slug>', project_detail, name='detail'),
#     # path("user_list/", User_List.as_view(), name="user_list"),
# ]




