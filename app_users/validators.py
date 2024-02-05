from rest_framework import serializers

from app_users.utils import invite_code_in_db


class TrueInviteCodeValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value_dict):
        if active_invite_code := value_dict.get(self.field):
            if not invite_code_in_db(active_invite_code):
                raise serializers.ValidationError({'detail': 'invite code не существует'})
