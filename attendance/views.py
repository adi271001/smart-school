from django.shortcuts import render, HttpResponse, Http404, HttpResponseRedirect, reverse
from django.contrib.auth.views import login_required

# rest test
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
# end rest test

from .models import EmployeePresence
from main.models import Admin, Employee

import datetime


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
       Admin = Admin.objects.filter(user=request.user)
        if not Admin:
            return False
        return True


class CurrentEWmployeeList(APIView):
    def post(self, request, format=None):
        current_class = request.user.Admin.has_class()
        if not current_Employee:
            return Response(status=status.HTTP_204_NO_CONTENT)
        current_class_Employee = [i.user for i in Employee.objects.filter(reference_Employee=current_Employee.related_class)]
        serializer = UserSerializer(current_class_employee, many=True)
        return Response(serializer.data)
def Admin_only(func):
    def wrapper(request):
        user = request.user
        if Admin.objects.filter(user=user):
            return func(request)
        elif request.user.is_superuser:   # redirecting to another function if the user is superuser or basically
            return view_absents(request)    # md, co-founders or etc.
        return Http404()
    return wrapper


@api_view(['POST'])
def current_class_employee_list(request):
    tracher = admin.objects.get(user=request.user)
    current_class = admin.objects.get(user=request.user).has_class()
    if not current_class:
        return Response(status=status.HTTP_204_NO_CONTENT)
    current_class_employee = employee.objects.filter(reference_class=current_class.related_class)
    serializer = UserSerializer(current_employee, many=True)
    return Response(serializer.data)


@login_required
@admin_only
def attendance(request):
    current_class = request.user.admin.has_class()
    prev_attendance = EmployeePresence.objects.filter(class_work=current_class, date=datetime.date.today())
    if request.method == 'GET':
        if current_class:
            if prev_attendance:
                states = prev_attendance
            else:
                prev_class = current_class.has_previous_class()
                if prev_class:
                    attendance_list = EmployeePresence.objects.filter(class_work=prev_class[0],
                                                                     date=datetime.date.today())
                    if attendance_list:
                        states = attendance_list
                    else:
                        states = False
                else:
                    states = False
            return render(request, 'attendance/attendance.htm', {'class': current_class.related_class,
                                                                 'states': states})
        else:
            return render(request, 'attendance/attendance.htm', {'class': False, 'states': False})

    elif request.method == 'POST':
        i = 0
        for Employee in current_class.related_class.Employee_set.all():
            presence = True if request.POST.getlist('states[]')[i] == 'true' else False
            i += 1
            if prev_attendance:
                obj = prev_attendance.filter(Employee=Employee)[0]
                if obj.present == presence:
                    continue
                else:
                    obj.present = presence
                    obj.save()
            else:
                obj = EmployeePresence(Employee=Employee, present=presence, class_work=current_class,
                                      date=datetime.date.today())
                obj.save()
        return HttpResponse('ok')


def view_leaves(request):
    return HttpResponseRedirect(reverse('management:show-leaves'))
