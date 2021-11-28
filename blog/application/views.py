from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import generic as gc

from django.conf import settings as st

from . import models as ml
from . import forms as fm


class Index(gc.ListView):
    """- Главной страницы"""
    paginate_by = st.NUMBER_PAGE
    model = ml.Article
    template_name = "index.html"
    context = "Blog Application"

    def get_queryset(self):
        """- переопределяем запрос к базе"""
        return ml.Article.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        # переопределяем контекст запроса, добавляем title
        context = super().get_context_data(**kwargs)
        context["title"] = self.context
        return context


class AuthorContent(gc.ListView):
    """- Все страницы автора"""
    model = ml.Article
    template_name = "content_author.html"
    context = "Все страницы автора"

    def get_queryset(self):
        """- переопределяем запрос к базе"""
        print(self.kwargs.get("author"))
        return ml.Article.objects.filter(author=self.kwargs.get("auth_id"))

    def get_context_data(self, *, object_list=None, **kwargs):
        # переопределяем контекст запроса, добавляем title
        context = super().get_context_data(**kwargs)
        context["title"] = self.context
        return context


class ShowArticle(gc.DetailView):
    """- Просмотр статьи"""
    model = ml.Article
    template_name = "show.html"


class AuthorArticles(LoginRequiredMixin, gc.ListView):
    """- Статьи Автора"""
    model = ml.Article
    template_name = "author.html"
    context = "Статьи автора"

    def get_queryset(self):
        """- переопределяем запрос к базе"""
        return ml.Article.objects.filter(author=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        # переопределяем контекст запроса, добавляем title
        context = super().get_context_data(**kwargs)
        context["title"] = self.context
        return context


class DeleteArticle(LoginRequiredMixin, gc.DeleteView):
    """- Удалить статью"""
    model = ml.Article
    success_url = reverse_lazy('author')
    template_name = 'delete.html'


class EditArticle(LoginRequiredMixin, gc.UpdateView):
    """- Редактировать статью"""
    model = ml.Article
    form_class = fm.CreateArticleForm
    success_url = reverse_lazy('author')
    template_name = 'edit.html'


class CreateArticle(LoginRequiredMixin, gc.CreateView):
    """- Добавить новую статью"""
    model = ml.Article
    form_class = fm.CreateArticleForm
    success_url = reverse_lazy('create')
    template_name = 'create.html'

    def form_valid(self, form):
        """- Передача текущего пользователя в базу"""
        form.instance.author = self.request.user
        return super().form_valid(form)


class Login(LoginView):
    """- Пройти аутентификацию"""
    form_class = fm.LoginForm
    success_url = reverse_lazy('index')
    template_name = 'login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """- Покинуть страницу пользователя"""
    template_name = 'index.html'

