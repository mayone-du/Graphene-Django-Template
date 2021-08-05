import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.signing import dumps, loads
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from .models import Profile, Task, TestModel, User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            'username': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'is_staff': ['exact']
        }
        interfaces = (relay.Node,)


class CreateUserMutation(relay.ClientIDMutation):
    class Input:
        username = graphene.String(required=False)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserNode)

    def mutate_and_get_payload(root, info, **input):
        user = User(
            email=input.get('email'),
        )
        user.username = input.get('username')
        user.set_password(input.get('password'))
        token = dumps(user.pk)
        send_mail(subject='サンプルアプリ | 本登録のお知らせ', message=f'ユーザー作成時にメール送信しています\n{token}' + input.get('email'), from_email="sample@email.com",
            recipient_list=[input.get('email')], fail_silently=False)

        user.save()

        return CreateUserMutation(user=user)



# メールでの本登録
class UpdateUserMutation(relay.ClientIDMutation):
    class Input:
        token = graphene.String(required=True)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, **kwargs):
        token = kwargs.get('token')
        # 受け取ったトークンからユーザーIDを取得
        user_pk = loads(token)
        user = get_user_model().objects.get(pk=user_pk)
        # ユーザーが存在しなかったらエラー
        if user is None:
            raise
        # TODO: userのis_activeをTrueにする
        ok = True
        return UpdateUserMutation(ok=ok)

class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        filter_fields = {
            'profile_name': ['exact', 'icontains'],
            'profile_text': ['exact', 'icontains']
        }
        interfaces = (relay.Node,)


class ProfileCreateMutation(relay.ClientIDMutation):
    class Input:
        # target_user = graphene.ID
        profile_name = graphene.String(required=True)
        profile_text = graphene.String(required=False)

    profile = graphene.Field(ProfileNode)

    def mutate_and_get_payload(root, info, **input):
        profile = Profile(
            profile_name=input.get('profile_name'),
        )
        profile.profile_text = input.get('profile_text')
        profile.save()

        return ProfileCreateMutation(profile=profile)


class SendEmail(relay.ClientIDMutation):
    ok = graphene.Boolean()
    @staticmethod
    def mutate(root, info):
        ok = True
        return SendEmail(ok=ok)

class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    create_profile = ProfileCreateMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


class Query(graphene.ObjectType):
    user = graphene.Field(UserNode, id=graphene.NonNull(graphene.ID))
    all_users = DjangoFilterConnectionField(UserNode)
    profile = graphene.Field(ProfileNode, id=graphene.NonNull(graphene.ID))
    all_profiles = DjangoFilterConnectionField(ProfileNode)

    @login_required
    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        return get_user_model().objects.get(id=from_global_id(id)[1])

    @login_required
    def resolve_all_users(self, info, **kwargs):
        return get_user_model().objects.all()

    @login_required
    def resolve_profile(self, info, **kwargs):
        id = kwargs.get('id')
        return Profile.objects.get(id=from_global_id(id)[1])

    @login_required
    def resolve_all_profiles(self, info, **kwargs):
        return Profile.objects.all()
