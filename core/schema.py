import graphene
from graphene_django import \
    DjangoObjectType  # used to change Django object into a format that is readable by GraphQL

from apps.common.models import Contact


class ContactType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = Contact
        field = ("id", "name", "phone_number")


class Query(graphene.ObjectType):
    # query ContactType to get list of contacts
    list_contact = graphene.List(ContactType)

    get_contact = graphene.Field(ContactType, id=graphene.Int())

    def resolve_list_contact(root, info):
        # We can easily optimize query count in the resolve method
        return Contact.objects.all()

    def resolve_get_contact(root, info, id):
        try:
            return Contact.objects.get(pk=id)
        except Contact.DoesNotExist:
            return None


class ContactMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        phone_number = graphene.String(required=True)

    # The class attributes define the response of the mutation
    contact = graphene.Field(ContactType)

    def mutate(self, info, name, phone_number):
        contact = Contact.objects.create(name=name, phone_number=phone_number)
        # Notice we return an instance of this mutation
        return ContactMutation(contact=contact)


class Mutation(graphene.ObjectType):
    create_contact = ContactMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
