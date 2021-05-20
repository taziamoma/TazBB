from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from ckeditor.fields import RichTextField
from django.utils.functional import cached_property


# Create your models here.


# Extending user model
def user_post_count(user):
    post_count = Post.objects.filter(author=user).count()
    return post_count


def user_thread_count(user):
    thread_count = Thread.objects.filter(author=user).count()
    return thread_count


User.add_to_class('user_post_count', user_post_count)
User.add_to_class('user_thread_count', user_thread_count)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Forum(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='forums')

    def __str__(self):
        return self.name

    def total_threads(forum):
        thread_count = Thread.objects.filter(thread_forum=forum).count()
        return thread_count

    def total_posts(forum):
        threads = Thread.objects.filter(thread_forum=forum)
        post_counter = 0
        for thread in threads:
            post_counter = post_counter + Post.objects.filter(post_thread=thread).count()

        return post_counter

    def last_post_thread(forum):
        last_post_thread = Thread.objects.filter(thread_forum=forum).order_by('-id')[0].pk

        return last_post_thread

    def last_post_thread_name(forum):
        last_post_thread_name = Thread.objects.filter(thread_forum=forum).order_by('-id')[0].name

        return last_post_thread_name

    def last_post_thread_author(forum):
        last_post_thread_author = Thread.objects.filter(thread_forum=forum).order_by('-id')[0].author

        return last_post_thread_author

    def last_post_thread_author_id(forum):
        last_post_thread_author_id = Thread.objects.filter(thread_forum=forum).order_by('-id')[0].author.id

        return last_post_thread_author_id


class Thread(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    thread_forum = models.ForeignKey(Forum, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def thread_reply_count(thread):
        thread_reply_count = Post.objects.filter(post_thread=thread).count() - 1
        return thread_reply_count

    def thread_last_reply_user(thread):
        last_reply = Post.objects.filter(post_thread=thread).order_by('-id')[0]
        thread_last_reply_user = last_reply.author
        return thread_last_reply_user

    def thread_get_userid(thread):
        last_reply = Post.objects.filter(post_thread=thread).order_by('-id')[0]
        thread_last_reply_user = last_reply.author
        thread_get_userid = thread_last_reply_user.id
        return thread_get_userid

    def thread_last_reply_date(thread):
        last_reply = Post.objects.filter(post_thread=thread).order_by('-id')[0]
        thread_last_reply_date = last_reply.post_date
        return thread_last_reply_date


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    post_body = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    post_thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' | ' + str(self.author)

    # @cached_property
    # def user_post_count(self):
    #    return self.author.post_set.filter(author=self.author).count()
