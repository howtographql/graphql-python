import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from links.models import Link, Vote
from users.schema import get_user, UserType


class LinkType(DjangoObjectType):
    search = graphene.String()

    class Meta:
        model = Link


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote


class Query(graphene.AbstractType):
    links = graphene.List(
        LinkType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    votes = graphene.List(VoteType)

    def resolve_links(self, args, context, info):
        search = args.get('search')
        first = args.get('first')
        skip = args.get('skip')

        qs = Link.objects.all()

        if search:
            filter = (
                Q(url__icontains=search) | 
                Q(description__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip::]

        if first:
            qs = qs[:first]

        return qs

    @graphene.resolve_only_args
    def resolve_votes(self):
        return Vote.objects.all()


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    class Input:
        url = graphene.String()
        description = graphene.String()

    @staticmethod
    def mutate(root, input, context, info):

        user = get_user(context) or None

        link = Link(
            url=input.get('url'),
            description=input.get('description'),
            posted_by=user,
        )
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by,
        )


class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Input:
        link_id = graphene.Int()

    @staticmethod
    def mutate(root, input, context, info):
        user = get_user(context) or None
        if not user:
            raise Exception('You must be logged to vote!')

        link = Link.objects.filter(id=input.get('link_id')).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)


class Mutation(graphene.AbstractType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()
