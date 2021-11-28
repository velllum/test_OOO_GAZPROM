from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from . import models
from .forms import LoginForm, CreateArticleForm


class Index(ListView):
    """- Главной страницы"""
    paginate_by = 6
    model = models.Article
    template_name = "index.html"
    context = "Blog Application"

    def get_queryset(self):
        return models.Article.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.context
        return context


class AuthorContent(ListView):
    """- Все страницы автора"""
    model = models.Article
    template_name = "content_author.html"
    context = "Все страницы автора"

    def get_queryset(self):
        print(self.kwargs.get("author"))
        return models.Article.objects.filter(author=self.kwargs.get("auth_id"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.context
        return context


class ShowArticle(DetailView):
    """- Просмотр статьи"""
    model = models.Article
    template_name = "show.html"


class AuthorArticles(LoginRequiredMixin, ListView):
    """- Статьи Автора"""
    model = models.Article
    template_name = "author.html"
    context = "Статьи автора"

    def get_queryset(self):
        return models.Article.objects.filter(author=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.context
        return context


class DeleteArticle(LoginRequiredMixin, DeleteView):
    """- Удалить статью"""
    model = models.Article
    success_url = reverse_lazy('author')
    template_name = 'delete.html'


class EditArticle(LoginRequiredMixin, UpdateView):
    """- Редактировать статью"""
    model = models.Article
    form_class = CreateArticleForm
    success_url = reverse_lazy('author')
    template_name = 'edit.html'


class CreateArticle(LoginRequiredMixin, CreateView):
    """- Добавить новую статью"""
    model = models.Article
    form_class = CreateArticleForm
    success_url = reverse_lazy('create')
    template_name = 'create.html'

    def form_valid(self, form):
        """- Передача текущего пользователя в базу"""
        form.instance.author = self.request.user
        return super().form_valid(form)


class Login(LoginView):
    """- Пройти аутентификацию"""
    form_class = LoginForm
    success_url = reverse_lazy('index')
    template_name = 'login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """- Покинуть страницу пользователя"""
    template_name = 'index.html'

