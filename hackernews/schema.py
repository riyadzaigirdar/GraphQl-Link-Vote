import graphene
import links.schema
import users.schema
import graphql_jwt
import links.schema_relay


class Query(links.schema_relay.RelayQuery, users.schema.Query, links.schema.Query, graphene.ObjectType):
    pass


class Mutation(links.schema_relay.RelayMutation, users.schema.Mutation, links.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
