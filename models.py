import datetime
from django.db import models
from django.forms.models import inlineformset_factory
from django.forms import ModelForm
from django.db.models import Q
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

# Create your models here.

class Branch(models.Model):
    name = models.CharField(max_length=160)
    location = models.CharField(max_length=80)
    details = models.TextField(max_length=400, blank=True, null=True)

class BranchForm(ModelForm):
    class Meta:
        model = Branch

class StaffManager(BaseUserManager):
    def create_user(self, name, mobile, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not mobile:
            raise ValueError('Users must have an mobile number')

        user = self.model(
            name=name,
            mobile=mobile,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, mobile, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(name=name,
            mobile=mobile,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#Levels can be senior, junior and midlevel
class Staff(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=40, blank=False)
    mobile = models.CharField(max_length=10, unique=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = StaffManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['name',]
    
    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.name

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
 
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Contact(models.Model):
    staff =  models.ForeignKey(Staff)
    contact_person = models.CharField(max_length=64, blank=True, null=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    type = models.CharField(max_length=16, blank=True, null=True)
    temp_address = models.TextField(blank=True, null=True)
    perm_address = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=80, blank=True, null=True)

class Supervisor(models.Model):
    staff = models.ForeignKey(Staff, related_name = 'staff')
    supervisor = models.ForeignKey(Staff, related_name = 'supervisor')
    start_date = models.DateField(default=datetime.datetime.now, null=True)
    end_date = models.DateField(blank=True, null=True)

class SupervisorForm(ModelForm):
    def __init__(self,mobile,*args,**kwargs):
        super (SupervisorForm,self ).__init__(*args,**kwargs)
        #Exclude Staffs who are already assigned with supervisors.
        exclude_staffs = Supervisor.objects.filter().values('staff')
        self.fields['staff'].queryset = Staff.objects.filter(groups__name='Nurse').filter(~Q(mobile=mobile)).exclude(id__in = exclude_staffs)

    class Meta:
        model = Supervisor
        fields = ('staff', 'start_date', 'end_date',)

class Personal_Details(models.Model):
    staff = models.ForeignKey(Staff)
    branch = models.ForeignKey(Branch, blank=True, null=True)
    full_name = models.CharField(max_length=120, blank=True, null=True)
    qualification = models.CharField(max_length=80, blank=True, null=True)
    doj = models.DateField(blank=True, null=True)
    dol = models.DateField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    hours_agreed = models.IntegerField(default=40)
    company_name = models.CharField(max_length=120, blank=True, null=True)
    designation = models.CharField(max_length=40, blank=True, null=True)
    department = models.CharField(max_length=64, blank=True, null=True)
    sub_department = models.CharField(max_length=64, blank=True, null=True)
    marital_status = models.CharField(max_length=16, blank=True, null=True)
    blood_group = models.CharField(max_length=16, blank=True, null=True)
    location = models.CharField(max_length=64, blank=True, null=True)
    employee_status = models.CharField(max_length=16, blank=True, null=True)
    employment_status = models.CharField(max_length=16, blank=True, null=True)

class DetailsForm(ModelForm):

    class Meta:
        model = Personal_Details

class Certification(models.Model):
    staff = models.ForeignKey(Staff)
    certified_on = models.DateField(blank=True, null=True)
    certification_name = models.CharField(max_length=120)
    certification_body = models.CharField(max_length=120, blank=True, null=True)
    valid_till = models.DateField(blank=True, null=True)

class Compensation(models.Model):
    staff = models.ForeignKey(Staff)
    basic = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    hra = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    conveyance = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    monthly = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    gross = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    bonus = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    pf = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    esi = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    other = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    renumeration = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    retention_bonus = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    individual_perf_pay = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    quarter_perf_pay = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    type = models.CharField(max_length=16, blank=True, null=True)

class Experience(models.Model):
    staff = models.ForeignKey(Staff)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    organization = models.CharField(max_length=120)
    address = models.CharField(max_length=300, blank=True, null=True)

class Ward(models.Model):
    branch = models.ForeignKey(Branch)
    name = models.CharField(max_length=80, blank=False)
    type = models.CharField(max_length=16)
    beds = models.IntegerField(default=0, blank=True, null=True)
    average_hours = models.IntegerField(default=0)
    seniors = models.IntegerField(default=0, blank=True, null=True)
    juniors = models.IntegerField(default=0, blank=True, null=True)
    midlevels = models.IntegerField(default=0, blank=True, null=True)

class WardForm(ModelForm):
    class Meta:
        model = Ward

class Ward_Staff(models.Model):
    staff =  models.ForeignKey(Staff)
    ward =  models.ForeignKey(Ward)
    duty_type = models.CharField(max_length=16, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

class WardStaffForm(ModelForm):
    class Meta:
        model = Ward_Staff

class Attendance(models.Model):
    staff =  models.ForeignKey(Staff)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField()
    day = models.DateField()
    duty_type = models.CharField(max_length=16, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance

class Leave(models.Model):
    staff = models.ForeignKey(Staff)
    approved_by = models.ForeignKey(Staff, related_name = 'approved_by', blank=True, null=True)
    leave_from = models.DateTimeField(blank=False)
    leave_to = models.DateTimeField(blank=False)
    applied_on = models.DateField(auto_now_add=True, blank=False)
    status = models.CharField(max_length=16, blank=True, null=True)
    approved_on = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    reason = models.TextField(blank=False)
    type = models.CharField(max_length=16, blank=False)

class LeaveForm(ModelForm):
    class Meta:
        model = Leave
        fields = ('type', 'leave_from', 'leave_to', 'reason')

class Roster(models.Model):
    ward = models.ForeignKey(Ward)
    title = models.CharField(max_length=160)
    description = models.CharField(max_length=240)
    planned_hours = models.IntegerField()
    actual_hours = models.IntegerField(null=True, blank=True)
    is_authorized = models.BooleanField(default=False)
    authorized_by = models.ForeignKey(Staff, related_name = 'authorized_by', blank=True, null=True)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    comments = models.TextField(blank=True, null=True)
    seniors = models.IntegerField(blank=True, null=True)
    juniors = models.IntegerField(blank=True, null=True)
    midlevels = models.IntegerField(blank=True, null=True)
    drafted_by = models.ForeignKey(Staff, related_name ='drafted_by')

class RosterForm(ModelForm):
    class Meta:
        model = Roster
        fields = ('ward', 'title', 'description', 'planned_hours', 'start_date', 'end_date', 'comments', 'seniors', 'juniors', 'midlevels',)

class Shift(models.Model):
    staff = models.ForeignKey(Staff)
    day = models.DateField(blank=False)
    roster = models.ForeignKey(Roster)
    start = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
    details = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=12, blank=False)

ShiftFormset = inlineformset_factory(Roster, Shift, fields=('staff', 'day', 'start', 'end', 'status', 'details', 'comments',), can_delete=False)
