from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from string import Template


# Author model
class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    # Calculates rating
    def update_rating(self):
        post_rating = self.post_set.aggregate(postRating=Sum('rating'))
        post_temp_rating = 0
        post_temp_rating += post_rating.get('postRating')
        comment_rating = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        comment_temp_rating = 0
        comment_temp_rating += comment_rating.get('commentRating')
        self.ratingAuthor = post_temp_rating * 3 + comment_temp_rating
        self.save()

    def __str__(self):
        return f'User {self.authorUser.username}'


# Category and tags
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


# Post and article
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # choices
    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGORY_CHOICES = (
        (ARTICLE, 'Article'),
        (NEWS, 'News')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    # Preview string template
    template_string = '$text...'

        # Rating modifiers
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # Post preview (using string templates)
    def preview(self):
        return Template(self.template_string).substitute(text=self.text[0:123])

    def __str__(self):
        return f'{self.title} {self.dateCreation}: {self.text[:20]}...'


# ManyToMany model
class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


# Comments
class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    # Rating modifiers
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.commentPost.title}: {self.commentUser.username}: {self.text[:20]}... {self.dateCreation}'
