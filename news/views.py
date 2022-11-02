from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render

from django.views.generic import View
from general.forms import SuscriberForm
from news.forms import CommentForm, ReplyForm

from news.models import Article, ArticleViews, Category, Comment

import sweetify

class Util:
    @staticmethod
    def suscribe(req):
        newsletter_form = SuscriberForm(req.POST) 
        if newsletter_form.is_valid():
            newsletter_form.save()
            sweetify.success(req, title="Suscribed!", text="Your suscription was successful", button="Ok", timer=3500, icon="success")
        else:
            sweetify.error(req, title="Something went wrong!", text="Please make sure you enter a correct email", button="Ok", timer=3500, icon="error")


class HomeView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all().select_related('category')
        slider_articles = articles[:5]
        square_articles = articles[:4]
        breaking_news = articles.filter(status='BREAKING')[:2]
        trending_articles = articles.filter(status='TRENDING')[:5]
        latest_articles = articles[:13]
        featured_articles = articles.filter(featured=True)[:15]
        categories = Category.objects.all()
        newsletter_form = SuscriberForm() 
        
        context = {
            'slider_articles': slider_articles, 'square_articles': square_articles,
            'breaking_news': breaking_news, 'trending_articles': trending_articles,
            'latest_articles': latest_articles, 'categories': categories, 
            'featured_articles': featured_articles, 'newsletter_form': newsletter_form
        }
        return render(request, 'news/main.html', context)

    def post(self, request, *args, **kwargs):
        Util.suscribe(request)
        return redirect('/')

class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all().select_related('category')
        trending_articles = articles.filter(status='TRENDING')[:5]
        categories = Category.objects.all()
        
        try:
            article = Article.objects.get(slug=self.kwargs.get('article_slug'))
        except Article.DoesNotExist:
            raise Http404()
        
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        if not ArticleViews.objects.filter(article=article, ip=ip).exists():
            ArticleViews.objects.create(article=article, ip=ip)
            article.views += 1
            article.save()

        newsletter_form = SuscriberForm() 
        comment_form = CommentForm()
        reply_form = ReplyForm()

        context = {
            'article': article, 'trending_articles': trending_articles, 'categories': categories,
            'comment_form': comment_form, 'reply_form': reply_form, 'newsletter_form': newsletter_form
        }
        return render(request, 'news/article-detail.html', context)

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        reply_form = ReplyForm(request.POST)
        try:
            article = Article.objects.get(slug=self.kwargs.get('article_slug'))
        except Article.DoesNotExist:
            raise Http404()
        if 'article_slug' in request.POST:
            if comment_form.is_valid():
                instance = comment_form.save(commit=False)
                instance.article = Article.objects.get(slug=request.POST.get('article_slug'))
                instance.save()
                return JsonResponse({
                    'name': instance.name, 'email': instance.email, 
                    'website': instance.website, 'message': instance.message
                })
            else:
                return JsonResponse({'error': 'Comment not submitted'})

        elif 'comment_id' in request.POST:
            if reply_form.is_valid():
                instance = reply_form.save(commit=False)
                instance.comment = Comment.objects.get(id=request.POST.get('comment_id'))
                instance.save()
                return JsonResponse({
                    'name': instance.name, 'email': instance.email, 'message': instance.message
                })
            else:
                return JsonResponse({'error': 'Comment not submitted'})
                
        else:
            Util.suscribe(request)
            return redirect(article.get_absolute_url)