from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


from user_app.api.serializers import RegistrationSerializer
from user_app import models


@api_view(['POST'])
def register_view(request):
    # if not request.data.get('password'):
    #     return Response({'error':'password not sent'})
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        if serializer.is_valid():
            user_obj = serializer.save()  #returned obj from serializer's save method
            data['username'] = user_obj.username
            data['email'] = user_obj.email
            data['response'] = 'Registration successful'

            token = Token.objects.get(user=user_obj).key
            data['token'] = token

        else:
            data = serializer.errors

        return Response(data,status=status.HTTP_201_CREATED)


@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        if request.user.is_anonymous:
            return Response({'error':'No credentials found'},status=status.HTTP_401_UNAUTHORIZED)

        request.user.auth_token.delete()
        return Response({'success':'You have successfully logged out'},status=status.HTTP_200_OK)