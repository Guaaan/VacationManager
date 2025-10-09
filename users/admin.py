# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

User = get_user_model()

# Si ya está registrado (p. ej. auth.UserAdmin), lo desregistramos primero.
# Esto evita el error AlreadyRegistered cuando el modelo fue registrado automáticamente.
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # ajusta los campos mostrados en la lista del admin
    list_display = ('username', 'email', 'first_name', 'last_name', 'vacation_days')
    # si quieres mostrar campos adicionales en el formulario del admin, extiende fieldsets según necesites
