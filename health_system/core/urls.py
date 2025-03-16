from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    
        # User Actions
    path('add_food_log/', views.add_food_log, name='add_food_log'),
    path('update_bmi/', views.update_bmi, name='update_bmi'),
    path('ask_query/', views.ask_query, name='ask_query'),
    
        # Coach Actions
    path('review_queries/', views.review_queries, name='review_queries'),
    path('review_bmi_feedback/', views.review_bmi_feedback, name='review_bmi_feedback'),
    
    path('register/', views.register_user, name='register'),
    path('register_coach/', views.register_coach, name='register_coach'),
    path('logout/', views.user_logout, name='logout'),
]
