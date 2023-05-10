from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from .serializers import AccountSerializer, TicketSerializer, ParkingLotSerializer
from .models import Account, Ticket, ParkingLot


# show all ticket
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def tickets_list(request):
    tickets = Ticket.objects.all()
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#create ticket
@api_view(['POST'])
def create_ticket(request):
    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#get ticket for hardware update it
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_ticket(request, license_plate):
    try:
        ticket = Ticket.objects.filter(license = license_plate).latest('id')
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = TicketSerializer(ticket)
    return Response(serializer.data, status=status.HTTP_200_OK)

#update ticket
@api_view(['PUT'])
def update_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id = ticket_id)
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = TicketSerializer(ticket, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# list accounts
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def accounts_list(request):
    tickets = Account.objects.all()
    serializer = AccountSerializer(tickets, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#update password
@login_required
@api_view(['PUT'])
def update_password(request, account_id):
    new_password = request.data.get('password')
    try:
        account = Account.objects.get(id = account_id)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    account.set_password(new_password)
    serializer = AccountSerializer(account, data=request.data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#parking lots list
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def parkinglots_list(request):
    parkinglots = ParkingLot.objects.all()
    serializer = ParkingLotSerializer(parkinglots, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#update status of parking lot
@api_view(['PUT'])
def update_status(request, parkinglot_id):
    try:
        parking_lot = ParkingLot.objects.get(id = parkinglot_id)
    except ParkingLot.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    parkinglot_status = parking_lot.isfree
    parking_lot.change_status(parkinglot_status)    
    serializer = ParkingLotSerializer(parking_lot, data=request.data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)