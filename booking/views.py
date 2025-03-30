from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignupForm
from .models import Room, Reservation, UserProfile
from datetime import datetime

def index(request):
    return render(request, 'booking/index.html')

def about(request):
    return render(request, 'booking/about.html')

def gallery(request):
    return render(request, 'booking/gallery.html')

def kontakt(request):
    return render(request, 'booking/kontakt.html')

def ubytovanie(request):
    rooms = Room.objects.all()
    return render(request, 'booking/ubytovanie.html', {'rooms': rooms})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('/moj_ucet/')
        else:
            messages.error(request, "Nespravne prihlasovacie udaje")
            return redirect('login')
    return render(request, 'booking/login.html')

@login_required
def create_reservation(request):
    if request.method == "POST":
        action = request.POST.get('action', '')
        if action == 'select_dates':
            check_in_str = request.POST.get('check_in')
            check_out_str = request.POST.get('check_out')
            if not (check_in_str and check_out_str):
                messages.error(request, "Prosím, zadajte dátum príchodu a odchodu.")
                return redirect('create_reservation')
            try:
                check_in_date = datetime.strptime(check_in_str, "%Y-%m-%d").date()
                check_out_date = datetime.strptime(check_out_str, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Neplatný formát dátumu.")
                return redirect('create_reservation')
            if check_out_date <= check_in_date:
                messages.error(request, "Dátum odchodu musí byť neskôr ako dátum príchodu.")
                return redirect('create_reservation')
            available_rooms = Room.objects.exclude(
                reservation__check_in__lt=check_out_date,
                reservation__check_out__gt=check_in_date
            )
            return render(request, 'booking/reservation_form.html', {
                'rooms': available_rooms,
                'check_in': check_in_str,
                'check_out': check_out_str
            })
        elif action == 'reserve_room':
            room_id = request.POST.get('room_id')
            check_in_str = request.POST.get('check_in')
            check_out_str = request.POST.get('check_out')
            if not (room_id and check_in_str and check_out_str):
                messages.error(request, "Chýbajú údaje pre rezerváciu.")
                return redirect('create_reservation')
            room = get_object_or_404(Room, id=room_id)
            try:
                check_in_date = datetime.strptime(check_in_str, "%Y-%m-%d").date()
                check_out_date = datetime.strptime(check_out_str, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Neplatný formát dátumu.")
                return redirect('create_reservation')
            overlapping = Reservation.objects.filter(
                room=room,
                check_in__lt=check_out_date,
                check_out__gt=check_in_date
            )
            if overlapping.exists():
                messages.error(request, "Táto izba je v danom termíne už obsadená.")
                return redirect('create_reservation')
            else:
                days = (check_out_date - check_in_date).days
                total_price = days * room.price_per_night
                reservation = Reservation.objects.create(
                    user=request.user,
                    room=room,
                    check_in=check_in_date,
                    check_out=check_out_date,
                    total_price=total_price
                )
                messages.success(request, "Rezervácia bola úspešne vytvorená.")
                return redirect('reservation_detail', reservation_id=reservation.id)
        else:
            messages.error(request, "Neznáma akcia.")
            return redirect('create_reservation')
    else:
        return render(request, 'booking/reservation_form.html')

@login_required
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    return render(request, 'booking/reservation_detail.html', {'reservation': reservation})

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, phone=form.cleaned_data.get('phone'))
            login(request, user)
            return redirect('moj_ucet')
    else:
        form = SignupForm()
    return render(request, 'booking/signup.html', {'form': form})

@login_required
def moj_ucet(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'booking/moj_ucet.html', {'user_profile': user_profile, 'reservations': reservations})

@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'booking/room_detail.html', {'room': room})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == "POST":
        reservation.delete()
        messages.success(request, "Rezervácia bola zrušená.")
        return redirect('moj_ucet')
    return redirect('moj_ucet')
