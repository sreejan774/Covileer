from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts import models
from django.contrib.auth.models import User
import json

# Create your views here.

def createRequestList():
    requests = models.UserRequest.objects.all()
    requestList = []
    for item in requests:
        if item.requestStatus == False:
            string = str(item.requestList)
            requests = json.loads(string)
            dict_item = {
                "id" : item.pk, 
                "name" : models.UserProfile.objects.get(pk = item.user).name ,
                "itemList" : requests ,
                "pincode" :  models.UserProfile.objects.get(pk = item.user).pincode ,
                "address" : models.UserProfile.objects.get(pk = item.user).address,
            }
            requestList.append(dict_item)
    return requestList
        
def createVolAcceptedList(volunteerId):
    list = models.Connection.objects.filter(volunteerId = volunteerId)
    acceptedList = []
    for item in list :
        userrequest = item.requestId   
        itemList = json.loads(userrequest.requestList)     
        dict_item = {
            "requestId" : userrequest.pk,
            "name" :  models.UserProfile.objects.get(pk = userrequest.user.pk).name,
            "itemList" : itemList,
            "pincode" : models.UserProfile.objects.get(pk = userrequest.user.pk).pincode,
            "address" : models.UserProfile.objects.get(pk = userrequest.user.pk).address
        }
        acceptedList.append(dict_item)
    return acceptedList

        
    

@login_required
def vhome(request):
    userProfile = models.UserProfile.objects.get(user = request.user)
    requestList = createRequestList()
    acceptedList = createVolAcceptedList(request.user.pk)

    context = {
        "name" : userProfile.name,
        "requestList" : requestList,
        "acceptedList" : acceptedList,
        "requestLen" : len(requestList),
        "acceptedLen" : len(acceptedList)
    }

    return render(request,'dashboard/vhome.html',context)


def createUserAcceptedList(user):
    userRequests = models.UserRequest.objects.filter(user = user,requestStatus = True)
    list = []
    for item in userRequests:
        volunteerId = models.Connection.objects.get(requestId = item.pk).volunteerId
        volunteer = models.User.objects.get(pk = volunteerId.pk)
        volunteerName = models.UserProfile.objects.get(pk = volunteer.pk).name
        dict_item = {
            "requestId" : item.pk,
            "volunteerName": volunteerName,
            "requestList": json.loads(item.requestList),
        }
        list.append(dict_item)
    return list

def createPendingRequestList(user):
    pendingRequests = models.UserRequest.objects.filter(user=user, requestStatus=False)

    list = []
    for item in pendingRequests:
        requestString = item.requestList 
        requestDict = json.loads(requestString)
        list.append(requestDict)
    return list




@login_required
def uhome(request):
    userProfile = models.UserProfile.objects.get(user=request.user)
    acceptedList = createUserAcceptedList(request.user)
    pendingRequestList = createPendingRequestList(request.user)
    context = {
        "name" : userProfile.name,
        "acceptedList" : acceptedList,
        "acceptedLen":len(acceptedList),
        "pendingRequestList" : pendingRequestList,
        "pendingRequestLen" : len(pendingRequestList)
    }
    return render(request,'dashboard/uhome.html',context)


@login_required
def createRequest(request,pk):
    if request.method == "POST":
        dict = request.POST
        requestList = {}
        total = len(dict)
        total = (total//2)
        count = 0 

        for i in range(total):
            itemname = "item"+str(i)
            quantityname = "quantity"+str(i)
            item = dict.get(itemname)
            quantity = dict.get(quantityname)
            requestList[item] = quantity

        requestString = json.dumps(requestList)
        # save the string made to model

        userRequest = models.UserRequest(
                        requestList = requestString,
                        requestStatus = False,
                        user = request.user
                    )
        userRequest.save()

        # redirect to user homepage 
        return redirect('uhome')

    context = {
        "name" : models.UserProfile.objects.get(pk = request.user.pk).name
    }
    return render(request,'dashboard/createrequest.html', context)

@login_required
def acceptRequest(request,pk):
    userRequest = models.UserRequest.objects.get(pk=pk)
    userRequest.requestStatus = True
    userRequest.save()
    connection = models.Connection(requestId = userRequest ,volunteerId = request.user)
    connection.save()
    return redirect('vhome')

@login_required
def markDelivered(request):
    if request.method == "POST":
        requestId = request.POST.get('button')
        requestInstance = models.Connection.objects.get(requestId = requestId)
        requestInstance.delete()

        userRequestInstance = models.UserRequest.objects.get(pk = requestId)
        userRequestInstance.delete()
        
    return redirect('uhome')


    
