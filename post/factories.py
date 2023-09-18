import factory
from django.contrib.auth.models import User
from .models import *
from authentication.factories import UserFactory


# I wrote this code

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence')
    content = factory.Faker('sentence')
    image = factory.django.ImageField(color='blue')


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    content = factory.Faker('sentence')


class LikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Like

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)

# end of code I wrote
