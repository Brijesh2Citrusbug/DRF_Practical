from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class EventView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        body = request.data
        print(body)
        return Response([], status=status.HTTP_201_CREATED)



