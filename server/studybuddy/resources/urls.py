from django.urls import path
from resources import views

app_name='resources'
urlpatterns = [
    path('',views.index,name="index"),

    path('<path:resource_path>/study-guides/', views.file_page, {'category': 'Study Guides'}, name="study_guides"),
    path('<path:resource_path>/lecture-notes/', views.file_page, {'category': 'Lecture Notes'}, name="lecture_notes"),
    path('<path:resource_path>/practice-exams/', views.file_page, {'category': 'Practice Exams'}, name="practice_exams"),
    path('<path:resource_path>/useful-websites/', views.file_page, {'category': 'Useful Websites'}, name="useful_websites"),

    path('form/', views.res_form, name='res_form'),

    path('save/<uuid:resource_uuid>/', views.save_resource, name='save_resource'),
    path('unsave/<uuid:resource_uuid>/', views.unsave_resource, name='unsave_resource'),

    path('download/<uuid:resource_uuid>/', views.download_resource, name='download_resource'),

    path('<path:resource_path>/<str:category>/', views.file_page, name="file_page"),
    path('<path:resource_path>/', views.category_page, name="category_page"),

]
