from django.urls import path, include
from . import views



app_name = 'Courses'
urlpatterns = [
    path('',views.index,name="index"),
    path('add',views.add,name="add"),
    path('<int:course_id>/detail',views.detail,name="detail"),
    path('<int:course_id>/chapter/<int:chapter_id>',views.chapterQuestions,name="chapter"),
    path('chapterAdd/<int:chapter_id>',views.chapterAdd,name="chapterAdd"),
    path('<int:course_id>/exam',views.generateExam,name="exam"),
    path('<int:course_id>/generation',views.generation,name="generation"),
]
