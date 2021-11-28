from django.urls import path

from . import views


urlpatterns = [
    # вывод статей
    path('', views.Index.as_view(), name='index'),
    # аутентификация пользователя
    path('login/', views.Login.as_view(), name='login'),
    # покинуть страницу пользователя
    path('logout/', views.Logout.as_view(), name='logout'),
    # редактировать
    path('edit/<slug>/', views.EditArticle.as_view(), name='edit'),
    # удалить
    path('delete/<slug>/', views.DeleteArticle.as_view(), name='delete'),
    # создать
    path('create/', views.CreateArticle.as_view(), name='create'),
    # страница аутентифицированного пользователя, с его статьями
    path('author/', views.AuthorArticles.as_view(), name='author'),
    # стать автора
    path('author-content/<auth_id>', views.AuthorContent.as_view(), name='author_content'),
    # все статьи
    path('<slug>/', views.ShowArticle.as_view(), name='show'),
]


