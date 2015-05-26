from recruit_app.user.models import EveCharacter, EveAllianceInfo, EveApiKeyPair, EveCorporationInfo
from recruit_app.user.models import User, Role, roles_users, AuthInfo
from flask_security import current_user
from recruit_app.admin import AuthenticatedModelView


def register_admin_views(admin, db):
    admin.add_view(EveCharacterAdmin(EveCharacter, db.session, category='EvE'))
    admin.add_view(EveCorporationInfoAdmin(EveCorporationInfo, db.session, category='EvE'))
    admin.add_view(EveAllianceInfoAdmin(EveAllianceInfo, db.session, category='EvE'))
    admin.add_view(EveApiKeyPairAdmin(EveApiKeyPair, db.session, category='EvE'))
    admin.add_view(UserAdmin(User, db.session, endpoint="users", category='Users'))
    admin.add_view(RoleAdmin(Role, db.session, category='Users'))
    admin.add_view(AuthInfoAdmin(AuthInfo, db.session, category='Users'))


class AuthInfoAdmin(AuthenticatedModelView):
    searchable = ('user.username',
                  'user.email',
                  'main_character.character_name',
                  'id',
                  )
    # show = ('api_id', 'api_key', 'user.auth_info.main_character.character_name', 'user.username', 'user.email')
    column_list = searchable
    column_sortable_list = searchable
    column_auto_select_related = True
    # column_display_all_relations = True
    column_searchable_list = searchable
    column_filters = searchable


class EveCharacterAdmin(AuthenticatedModelView):
    column_auto_select_related = True
    # column_display_all_relations = True
    searchable = (EveCharacter.character_name,
                  EveCharacter.character_id,
                  'alliance.alliance_name',
                  'corporation.corporation_name',
                  'corporation.corporation_id',
                  'user.email',
                  'user.username',
                  'api.api_id')
    column_searchable_list = searchable
    column_filters = searchable


class EveCorporationInfoAdmin(AuthenticatedModelView):
    column_auto_select_related = True
    # column_display_all_relations = True
    searchable = (EveCorporationInfo.corporation_name,
                  EveCorporationInfo.corporation_id,
                  EveCorporationInfo.corporation_ticker,
                  'alliance.alliance_id',
                  'alliance.alliance_name',)
    column_searchable_list = searchable
    column_filters = searchable + ('member_count',)


class EveAllianceInfoAdmin(AuthenticatedModelView):
    column_auto_select_related = True
    # column_display_all_relations = True
    searchable = (EveAllianceInfo.alliance_id,
                  EveAllianceInfo.alliance_name,
                  EveAllianceInfo.alliance_ticker,
                  )
    column_searchable_list = searchable
    column_filters = searchable + ('member_count',)


class UserAdmin(AuthenticatedModelView):
    column_auto_select_related = True
    # column_display_all_relations = True
    searchable = ('username',
                  'email',
                  'characters.character_name',
                  )
    column_list = searchable + ('created_at',
                                'last_login_at',
                                'confirmed_at',
                                'active',
                                'login_count',
                                'last_login_ip',
                                'current_login_ip',)
    # column_sortable_list = searchable
    column_searchable_list = searchable
    column_filters = searchable + ('created_at',
                                   'last_login_at',
                                   'confirmed_at',
                                   'active',
                                   'login_count',
                                   'last_login_ip',
                                   'current_login_ip',)


class RoleAdmin(AuthenticatedModelView):
    column_auto_select_related = True
    # column_display_all_relations = True
    searchable = (Role.name,
                  Role.description,
                  )
    column_searchable_list = searchable
    column_filters = searchable


class EveApiKeyPairAdmin(AuthenticatedModelView):
    searchable = ('api_id',
                  'api_key',
                  'user.username',
                  'user.email',
                  'user.auth_info.main_character.character_name',
                  )
    # show = ('api_id', 'api_key', 'user.auth_info.main_character.character_name', 'user.username', 'user.email')
    column_list = searchable
    column_sortable_list = searchable
    column_auto_select_related = True
    # column_display_all_relations = True
    column_searchable_list = searchable
    column_filters = searchable + ('last_update_time',
                                   'valid')


def check_if_admin():
    if current_user:
        if current_user.has_role("admin"):
            return True
        else:
            return False
    else:
        return False
