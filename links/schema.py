import graphene
from graphene_django import DjangoObjectType
from .models import Link, Votes
from users.schema import UserType

# link list QUERY starts


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class VotesType(DjangoObjectType):
    class Meta:
        model = Votes


class Query(graphene.ObjectType):
    links = graphene.List(LinkType, first=graphene.Int(), skip=graphene.Int())
    votes = graphene.List(VotesType, search=graphene.Int())

    def resolve_links(self, info, first=None, skip=None):
        qs = Link.objects.all()
        if skip:
            qs = qs[skip:]
        if first:
            qs = qs[:first]
        return qs

    def resolve_votes(self, info, search=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must me logged in to see list of votes")
        if search:
            if Link.objects.get(id=search):
                return Votes.objects.filter(link__id=search)
            else:
                raise Exception("link id does not exist")
        return Votes.objects.all()


# list QUERY ends

# link create MUTATION starts


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        user = info.context.user
        if user.is_anonymous:
            user = None
        link = Link(url=url, description=description, posted_by=user)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=user
        )
# link create MUTATION end

# vote create MUTATION starts


class CreateVote(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    user = graphene.String()

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user is None:
            raise Exception("You have to log in to cast a vote")
        link = Link.objects.get(pk=link_id)
        if not link:
            raise Exception("link not available | invalid link id")
        vote = Votes.objects.create(user=user, link=link)
        vote.save()
        return CreateVote(
            id=vote.id,
            url=link.url,
            user=user.username
        )

# vote create MUTATION ends


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()
