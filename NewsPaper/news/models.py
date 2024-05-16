from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        article_ratings_sum = sum(post.rating * 3 for post in self.post_set.all())
        comment_ratings_sum = sum(comment.rating for comment in self.user.comment_set.all())
        article_comments_ratings_sum = \
            sum(comment.rating for post in self.post_set.all() for comment in post.comment_set.all())
        self.rating = article_ratings_sum + comment_ratings_sum + article_comments_ratings_sum
        self.save()


class Category(models.Model):
    Sport = 'SP'
    Politics = 'PO'
    Economics = 'EC'
    Science = 'SC'
    Culture = 'CU'
    Religion = 'RE'
    Cooking = 'CO'
    Other = 'OT'

    CATEGORY = [
        (Sport, 'Спорт'),
        (Politics, 'Политика'),
        (Economics, 'Экономика'),
        (Science, 'Наука'),
        (Culture, 'Культура'),
        (Religion, 'Религия'),
        (Cooking, 'Кулинария'),
        (Other, 'Другое'),
    ]
    name = models.CharField(max_length=2,
                            unique=True,
                            choices=CATEGORY,
                            default=Other)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice = models.BooleanField(default=False)  # False = Статья True = Новость
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.TextField(max_length=120)
    text = models.TextField(max_length=10000)
    rating = models.IntegerField(default=0)

    def like_pos(self):
        self.rating += 1
        self.save()

    def dislike_pos(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[:124]}..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like_comm(self):
        self.rating += 1
        self.save()

    def dislike_comm(self):
        self.rating -= 1
        self.save()
