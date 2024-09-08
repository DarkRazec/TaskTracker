from django.urls import path
from rest_framework.routers import DefaultRouter

from tasks.apps import TasksConfig
from tasks.views import TaskViewSet, ImportantTasksListAPIView

app_name = TasksConfig.name

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('tasks/important/', ImportantTasksListAPIView.as_view(), name='important_tasks')
              ] + router.urls
