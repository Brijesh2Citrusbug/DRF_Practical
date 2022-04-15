
from django.http import Http404
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *


# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


class RegisterView(APIView):
    """
    User register here.
    """
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'data': serializer.data, 'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    User login here.
    """
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'msg': 'Login Successfully', 'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Not Found '}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventList(APIView):
    """
    List all events, or create a new event.
    """
    def get(self, request):
        queryset = EVENT.objects.all()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):

        name = request.data['name']
        address = request.data['address']
        organiser_name = request.data['organiser_name']
        organiser_email = request.data['organiser_email']
        data = request.data['data']

        event = EVENT.objects.create(name=name, address=address, organiser_name=organiser_name,
                                     organiser_email=organiser_email)

        for item in range(len(data)):
            event_date = EVENT_DATE.objects.create(event=event, date=data[item]['date'])

            for j in data:
                print(j['start_slot'])

        # serializer = EventSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventView(APIView):
    """
    Retrieve, update or delete a event instance.
    """
    # permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return EVENT.objects.filter(pk=pk)
        except EVENT.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        queryset = self.get_object(pk)
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        name = request.data['name']
        address = request.data['address']
        organiser_name = request.data['organiser_name']
        organiser_email = request.data['organiser_email']
        data = request.data['data']
        print(data)

        event = EVENT.objects.create(name=name, address=address, organiser_name=organiser_name,
                                     organiser_email=organiser_email)

        for item in range(len(data)):
            event_date = EVENT_DATE.objects.create(event=event, date=data[item]['date'])

            for i in item:
                print(i['start_slot'])

        # serializer = EventSerializer(data=request.data)
        # if serializer.is_valid():
        #     event = serializer.save()
        #     return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        # return Response({serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        queryset = self.get_object(pk)
        serializer = EventSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



