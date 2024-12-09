from rest_framework import views, status
from rest_framework.response import Response
from .models import User, Referral
from .serializers import UserSerializer
import time


class PhoneNumberAuthAPIView(views.APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        # Имитация отправки
        time.sleep(2)

        # Проверка или создание пользователя
        user, created = User.objects.get_or_create(phone_number=phone_number)

        return Response({'message': 'Код отправлен на номер телефона.'}, status=status.HTTP_200_OK)


class VerifyCodeAPIView(views.APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')  # тут нужно проверить код

        return Response({'message': 'Авторизация успешна.'}, status=status.HTTP_200_OK)


class UserProfileAPIView(views.APIView):
    def get(self, request):
        phone_number = request.query_params.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone_number)
            serializer = UserSerializer(user)
            # Получаем список пользователей, которые использовали ваш инвайт-код
            referrals = user.referrals.all()
            referred_numbers = [referral.referred_user.phone_number for referral in referrals]
            return Response({
                'user_data': serializer.data,
                'referred_users': referred_numbers  # Список номеров телефонов пользователей
            })
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        phone_number = request.data.get('phone_number')
        invite_code = request.data.get('invite_code')

        try:
            user = User.objects.get(phone_number=phone_number)
            if user.activated_invite_code is None:
                # Проверка на существование инвайт-кода
                referrer = User.objects.filter(invite_code=invite_code).first()
                if referrer:
                    user.activated_invite_code = invite_code
                    user.save()
                    Referral.objects.create(referrer=referrer, referred_user=user)
                    return Response({'message': 'Инвайт-код активирован.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Инвайт-код не существует.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {'message': 'Инвайт-код уже активирован.', 'activated_invite_code': user.activated_invite_code})

        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)