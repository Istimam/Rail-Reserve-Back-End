from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AdminPasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django import forms
from django.urls import path
from .models import CustomUser

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    is_active = forms.BooleanField(label='Active', initial=True, required=False)

    class Meta:
        model = CustomUser
        fields = ('phone_no', 'email', 'is_active')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('phone_no', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ('phone_no', 'email', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('phone_no', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_no', 'email', 'password1', 'password2', 'is_active'),
        }),
    )
    search_fields = ('phone_no', 'email')
    ordering = ('phone_no',)
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('date_joined',)

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return self.add_form
        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_urls(self):
        return [
            path('<id>/password/', self.admin_site.admin_view(self.change_password), name='auth_user_password_change'),
        ] + super().get_urls()

    def change_password(self, request, id, form_url=''):
        user = self.get_object(request, id)
        if not self.has_change_permission(request, user):
            raise PermissionDenied
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                msg = 'Password changed successfully.'
                self.message_user(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)
        context = {
            'title': 'Change password: {}'.format(user),
            'form': form,
            'form_url': form_url,
            'opts': self.model._meta,
            'original': user,
        }
        return TemplateResponse(request, 'admin/auth/user/change_password.html', context)

admin.site.register(CustomUser, CustomUserAdmin)
