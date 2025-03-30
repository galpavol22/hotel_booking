from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Room, Reservation, HotelInfo, UserProfile

# UserProfile inline admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

# Custom User admin
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Registrácia nového admin rozhrania pre User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Admin pre model Room – POZOR, správne polia podľa models.py
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price_per_night')

# Admin pre model Reservation – správne polia podľa models.py
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out')

# Admin pre model HotelInfo – správne polia podľa models.py
class HotelInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'address', 'phone', 'email')

# Admin pre UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')

# Registrácia admin rozhraní
admin.site.register(Room, RoomAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(HotelInfo, HotelInfoAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
