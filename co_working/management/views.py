from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
import datetime

from management.models import Member, Zone, SeatBooking
# Create your views here.


# login
def user_login(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password!'

    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url

    return render(request, template_name='login.html', context=context)


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


def sign_up(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        # user.first_name = request.POST.get('first_name')
        # user.last_name = request.POST.get('last_name')
        # user.email = request.POST.get('email')
        user.save()
        context['success'] = 'Successfully registered'
    else:
        context['error'] = 'Something went wrong or Password does not match'

    return render(request, template_name='login.html', context=context)


@login_required
def index(request):
    members = Member.objects.all()
    context = {
        'members': members
    }
    return render(request, template_name='index.html', context=context)


@login_required
def topup(request):
    return render(request, template_name='topup.html')


@login_required
def member_regis(request):
    msg = ''
    context = {}
    if request.method == 'POST':
        member_fname = request.POST.get('member_first_name')
        member_lname = request.POST.get('member_last_name')
        member = Member.objects.create(
            first_name=member_fname,
            last_name=member_lname,
            money=100
        )
        member.save()
        msg = 'Successfully registered Member: คุณ %s' % (member.first_name)
    else:
        context['error'] = 'Something went wrong please try again'

    context = {
        'msg': msg
    }

    return render(request, template_name='register_member.html', context=context)


@login_required
def check_in(request):

    now = datetime.datetime.now()
    zones = Zone.objects.all()
    members = Member.objects.all()
    msg = ''

    if request.method == 'POST':
        seat_booking = SeatBooking.objects.create(
            member_id=request.POST.get('member_id'),
            zone_id=request.POST.get('zone_id'),
            create_by_id=request.POST.get('create_by_id'),
            time_in=request.POST.get(now),
            time_out=request.POST.get('time_out'),
            total_price=request.POST.get('total_price'),
            create_date=request.POST.get('create_date')
        )
        msg = 'Successfully Check-in Member: คุณ %s เวลา: %s' % (
            members.filter(id=member_id).first_name, now)
    else:
        seat_booking = SeatBooking.objects.none()

    context = {
        'zones': zones,
        'seat_booking': seat_booking,
        'now': now,
        'members': members,
        'msg': msg
    }
    return render(request, template_name='index.html', context=context)


@login_required
def check_out(request, member_first_name):
    return redirect(to='index.html')
