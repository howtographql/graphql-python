import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import authenticate

from users.models import User


def get_user(context):
    token = context.session.get('token')

    if not token:
        return

    try:
        user = User.objects.get(token=token)
        return user
    except:
        raise Exception('User not found!')


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    @graphene.resolve_only_args
    def resolve_users(self):
        return User.objects.all()

    def resolve_me(self, args, context, info):
        user = get_user(context)
        if not user:
            raise Exception('Not logged!')

        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @staticmethod
    def mutate(root, input, context, info):
        username = input.get('username')
        password = input.get('password')
        email = input.get('email')

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class LogIn(graphene.Mutation):
    user = graphene.Field(UserType)

    class Input:
        username = graphene.String()
        password = graphene.String()

    @staticmethod
    def mutate(root, input, context, info):
        user = authenticate(
            username=input.get('username'),
            password=input.get('password'),
        )

        if not user:
            raise Exception('Invalid username or password!')

        context.session['token'] = user.token
        return LogIn(user=user)


class Mutation(graphene.AbstractType):
    create_user = CreateUser.Field()
    login = LogIn.Field()
