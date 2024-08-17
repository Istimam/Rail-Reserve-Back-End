from django.contrib import admin
from .models import NIDModel

class NIDModelAdmin(admin.ModelAdmin):
    list_display = ('id_number', 'id_name', 'id_gender', 'id_father_name', 'id_mother_name', 'id_date_of_birth', 'id_address')
    readonly_fields = ('id_number',)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields.remove('id_number')
        return fields

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return []

admin.site.register(NIDModel, NIDModelAdmin)
