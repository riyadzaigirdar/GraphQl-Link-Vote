import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Link, Votes


# 1
class LinkFilter(django_filters.FilterSet):
    class Meta:
        model = Link
        fields = ['url', 'description']


# 2
class LinkNode(DjangoObjectType):
    class Meta:
        model = Link
        # 3
        interfaces = (graphene.relay.Node, )


# class VoteNode(DjangoObjectType):
#     class Meta:
#         model = Vote
#         interfaces = (graphene.relay.Node,)


class RelayQuery(graphene.ObjectType):
    # 4
    relay_link = graphene.relay.Node.Field(LinkNode)
    # 5
    relay_links = DjangoFilterConnectionField(
        LinkNode, filterset_class=LinkFilter)


class RelayCreateLink(graphene.ClientIDMutation):
    link = graphene.Field(LinkNode)

    class Input:
        url = graphene.String()
        description = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user
        url = input.get("url")
        description = input.get("description")

        link = Link.objects.create(
            url=url,
            description=description
        )

        return RelayCreateLink(
            link=link
        )


class RelayMutation(graphene.AbstractType):
    relay_create_link = RelayCreateLink.Field()
