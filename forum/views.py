from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator


class HomeView(ListView):
    context_object_name = 'name'
    template_name = 'index.html'
    queryset = Category.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        categorys = Category.objects.all()


        context['categorys'] = categorys

        # Side bar statisitcs
        context['thread_count'] = Thread.objects.all().count()
        context['post_count'] = Post.objects.all().count()
        context['user_count'] = User.objects.all().count()
        #context['newest_user'] = User.objects.order_by('-id')[0]
        # Side bar statisitcs

        return context

class ThreadlistView(ListView):
    model = Thread
    context_object_name = 'threads'
    template_name = 'thread/threadlist.html'
    paginate_by = 10

    def get_queryset(self):
        self.forum = self.kwargs['forum']
        queryset = Thread.objects.filter(thread_forum=self.forum).order_by('-date')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ThreadlistView, self).get_context_data(*args, **kwargs)
        forum = Forum.objects.get(pk=self.forum)
        context['forum'] = forum
        return context


class ViewThreadView(ListView):
    model = Thread
    form_class = QuickReplyForm
    context_object_name = 'post_list'
    template_name = 'thread/viewthread.html'
    paginate_by = 10

    def get_queryset(self):
        self.thread = self.kwargs['thread']
        queryset = Post.objects.filter(post_thread=self.thread)
        return queryset

    def post(self, request, *args, **kwargs):
        quick_reply_user = request.user
        post_thread = Thread.objects.get(id=self.kwargs.get('thread', None))
        if request.method == "POST":
            quick_reply_form = QuickReplyForm(request.POST)

            if quick_reply_form.is_valid():
                post_content = quick_reply_form.cleaned_data['post_body']
                author = quick_reply_user
                post = Post(post_body=post_content, author=author, post_thread=post_thread)
                post.save()
                # return HttpResponseRedirect(request.path_info)  # redirect to same page

        else:
            quick_reply_form = QuickReplyForm(request.POST)

        return HttpResponseRedirect(request.path_info)  # redirect to same page

    def get_context_data(self, *args, **kwargs):
        context = super(ViewThreadView, self).get_context_data(*args, **kwargs)
        thread = Thread.objects.get(pk=self.thread)
        posts = Post.objects.filter(post_thread=self.thread)
        context['thread'] = thread
        context['posts'] = posts
        context['quick_reply_form'] = QuickReplyForm
        return context


class NewThreadView(CreateView):
    model = Thread
    form_class = NewThreadForm
    template_name = 'thread/newthread.html'

    def post(self, request, *args, **kwargs):
        thread_forum = Forum.objects.get(pk=self.kwargs.get('forum', None))

        thread_post_user = request.user
        if request.method == "POST":
            thread_form = NewThreadForm(request.POST)
            post_form = NewPostForm(request.POST)

            if thread_form.is_valid() and post_form.is_valid():
                thread = thread_form.save(commit=False)
                thread.thread_forum = thread_forum
                thread.author = thread_post_user
                thread = thread_form.save()

                post = post_form.save(False)

                post.post_thread = thread
                post.author = thread_post_user
                post.save()
        else:
            thread_form = NewThreadForm()
            post_form = NewPostForm()

        args = {}
        args.update(csrf(request))
        args['thread_form'] = thread_form
        args['post_form'] = post_form

        return HttpResponseRedirect(reverse('viewthread', args=[thread.id]))  # redirects to newly created thread

    def get_context_data(self, *args, **kwargs):
        context = super(NewThreadView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['forum'])
        context['forum'] = stuff.id
        context['thread_form'] = NewThreadForm
        context['post_form'] = NewPostForm
        return context


class MemberlistView(ListView):
    context_object_name = 'member_list'
    template_name = 'memberlist.html'
    paginate_by = 10

    def get_queryset(self):
        """Return Users"""
        return User.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(MemberlistView, self).get_context_data(*args, **kwargs)
        context['post_count'] = Post.objects.all().count()
        context['thread_count'] = Thread.objects.all().count()
        context['users'] = User.objects.all()

        return context


def UserProfileView(request, userid):
    user = User.objects.get(id=userid)

    return render(request, 'member.html', {'user': user})


class UserCPView(ListView):
    template_name = 'usercp/usercp.html'

    def get_queryset(self):
        pass

    def get_context_data(self, *args, **kwargs):
        context = super(UserCPView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        context['threads'] = Thread.objects.filter(author=user).order_by(('-date'))[:5]
        return context


class SearchView(FormView):
    template_name = 'search/search.html'
    form_class = SearchThreadsForm
    success_url = 'search-results'
    threads = Thread.objects.all()
    posts = Post.objects.all()

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            search_thread_form = SearchThreadsForm(request.POST)
            keywords = request.POST['keywords']
            authors = request.POST.get('authors', 'none')

        else:
            form = SearchThreadsForm()

        args = {}
        args.update(csrf(request))

        return HttpResponseRedirect(reverse('search-results', args=[keywords, authors]))

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context['search_thread_form'] = SearchThreadsForm
        return context


class SearchResultsView(ListView):
    template_name = 'search/results.html'

    def get_queryset(self):
        keywords = self.kwargs['keywords']
        author = User.objects.get(username=self.kwargs['author'])
        threads = Thread.objects.filter(name__contains=keywords, author=author).order_by('-date')

        return threads

    def get_context_data(self, *args, **kwargs):
        context = super(SearchResultsView, self).get_context_data(*args, **kwargs)
        context['threads'] = self.get_queryset()
        return context