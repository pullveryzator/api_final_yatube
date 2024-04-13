from rest_framework import validators
from rest_framework.serializers import (CurrentUserDefault, ModelSerializer,
                                        SlugRelatedField, ValidationError)

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'group', 'image', 'pub_date')


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'post')


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'posts')


class FollowSerializer(ModelSerializer):
    user = SlugRelatedField(
        slug_field='username', read_only=True, default=CurrentUserDefault())
    following = SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='На этого пользователя Вы уже подписаны!'
            )
        ]

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise ValidationError('Нельзя подписаться на самого себя!')
        return value
