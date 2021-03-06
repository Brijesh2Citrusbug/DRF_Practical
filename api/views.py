
from django.http import Http404
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import ListAPIView
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

    def get(self, request, pk):

        queryset = EVENT.objects.filter(pk=pk)
        serializer = EventSerializer(queryset, many=True)

        event_date = EVENT_DATE.objects.select_related('event').filter(event__pk=pk).distinct('date').values('date')
        date = EventDateSerializer(event_date, many=True)

        # access_point = EVENT_SLOT.objects.select_related('access_point').filter(event_date__event__pk=pk).distinct('access_point').values('access_point')
        # point = AccessPointSerialiser(access_point, many=True)
        # print(point.data)

        accesspoints = EVENT_SLOT.objects.filter(event_date__event=queryset.first()).values_list('access_point__name',
                                                                                                 flat=True).distinct()

        data= [serializer.data, date.data, list(accesspoints)]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):

        name = request.data['name']
        address = request.data['address']
        organiser_name = request.data['organiser_name']
        organiser_email = request.data['organiser_email']
        data = request.data['data']

        event = EVENT.objects.create(name=name, address=address, organiser_name=organiser_name,
                                     organiser_email=organiser_email)

        dates = [item['date'] for item in data]
        event_date = EVENT_DATE.objects.bulk_create(EVENT_DATE(event=event, date=i) for i in dates)

        for item in data:
        #     active_points = ACCESS_POINT.objects.filter(active=True)
        #     for point in item['access_points']:
        #         access_point = active_points.get(pk=point)
        #
        #         for time_slot in TIME.objects.filter(time__gte=item['start_slot']).filter(time__lt=item['end_slot']):
        #             event_slot = EVENT_SLOT.objects.bulk_create(EVENT_SLOT(time=time_slot, event_date=date,
        #                                                    access_point=access_point) for date in event_date)
        #
        #             slot_access = SLOT_ACCESS_POINTS.objects.bulk_create(SLOT_ACCESS_POINTS(slot=slot, access_point=access_point)
        #                                                                  for slot in event_slot)

            time_slot = TIME.objects.filter(time__gte=item['start_slot']).filter(time__lt=item['end_slot'])

            event_slot = EVENT_SLOT.objects.bulk_create(EVENT_SLOT(time=slot, event_date=date,access_point=ACCESS_POINT.objects.get(pk=point)) for slot in time_slot for date
                                                                in event_date for point in item['access_points'])

            slot_access = SLOT_ACCESS_POINTS.objects.bulk_create(SLOT_ACCESS_POINTS(slot=slot, access_point=ACCESS_POINT.objects.get(pk=point))
                                                                         for slot in event_slot for point in item['access_points'])

        return Response([], status=status.HTTP_201_CREATED)


class SlotBookView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        event_id = request.data['event_id']
        slot_id = request.data['slot_id']
        access_point = request.data['access_point']
        event = EVENT.objects.filter(pk=event_id)
        event_slot = EVENT_SLOT.objects.filter(pk=slot_id, event_date__event=event_id, access_point=access_point)

        if not event.exists():
            return Response("Event Not Found!")

        if not event_slot.exists():
            return Response("Slot for this event not found...!")

        for slot in event_slot:
            if slot.is_booked:
                return Response("This slot is already booked.")

            slot.is_booked = True
            slot.save()
        return Response({"event_id": event_id, "slot_id": slot_id}, status=status.HTTP_200_OK)


class AvailableSlotList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        event_id = self.request.query_params.get('event_id')
        available_slots = EVENT_SLOT.objects.filter(is_booked=False, event_date__event__pk=event_id).values('id')
        if not available_slots.exists():
            return Response("Event Not Found.")

        return Response(available_slots, status=status.HTTP_200_OK)


# class EventView(APIView):
#     """
#     Retrieve, update or delete a event instance.
#     """
#     # permission_classes = (IsAuthenticated,)
#
#     def get_object(self, pk):
#         try:
#             return EVENT.objects.filter(pk=pk)
#         except EVENT.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk):
#         queryset = self.get_object(pk)
#         serializer = EventSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         name = request.data['name']
#         address = request.data['address']
#         organiser_name = request.data['organiser_name']
#         organiser_email = request.data['organiser_email']
#         data = request.data['data']
#         print(data)
#
#         event = EVENT.objects.create(name=name, address=address, organiser_name=organiser_name,
#                                      organiser_email=organiser_email)
#
#         for item in range(len(data)):
#             event_date = EVENT_DATE.objects.create(event=event, date=data[item]['date'])
#
#             for i in item:
#                 print(i['start_slot'])
#
#         # serializer = EventSerializer(data=request.data)
#         # if serializer.is_valid():
#         #     event = serializer.save()
#         #     return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
#         # return Response({serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#
#
#     def put(self, request, pk):
#         queryset = self.get_object(pk)
#         serializer = EventSerializer(queryset, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         queryset = self.get_object(pk)
#         queryset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



