from rest_framework.permissions import BasePermission


class IsPhone(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.phone == obj.phone
