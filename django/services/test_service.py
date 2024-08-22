from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


class GetJwtService:
    def get_jwt(self, user_id: int):
        user = User.objects.get(pk=user_id)
        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}