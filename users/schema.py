import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

# Query


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()

    def resolve_me(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user

# Query Ends

# Mutation


class CreateUser(graphene.Mutation):
    id = graphene.Int()
    username = graphene.String()
    email = graphene.String()
    is_superuser = graphene.Boolean()

    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, username, email, password):
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(
            id=user.id,
            username=user.username,
            email=user.email,
            is_superuser=user.is_superuser,
        )


class UpdateUser(graphene.Mutation):
    updated_user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String()
        email = graphene.String()

    def mutate(self, info, username, email):
        user = info.context.user
        if user is None:
            raise Exception("You can only update your own credintials")
        user = get_user_model().objects.get(username=user.username)
        if user:
            user.username = username
            user.email = email
            user.save()
        return UpdateUser(updated_user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()


# Mutation Ends
