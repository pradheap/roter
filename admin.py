from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group, User
from staffing.models import Staff
# Register your models here.

class StaffAdmin(admin.ModelAdmin):
    list_display = ('mobile','name')

class GroupAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(queryset=Staff.objects.all(),
                                           widget=FilteredSelectMultiple('Users', False),
                                           required=False)
    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()

    def save(self, commit=True):
        group = super(GroupAdminForm, self).save(commit=commit)
        
        if commit:
            group.user_set = self.cleaned_data['users']
        else:
            old_save_m2m = self.save_m2m
            def new_save_m2m():
                old_save_m2m()
                group.user_set = self.cleaned_data['users']
            self.save_m2m = new_save_m2m
        return group

class MyGroupAdmin(GroupAdmin):
    form = GroupAdminForm

admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)
admin.site.register(Staff, StaffAdmin)
