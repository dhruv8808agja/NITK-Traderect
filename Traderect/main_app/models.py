# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Need(models.Model):
    nid = models.IntegerField(primary_key=True)
    productname = models.CharField(db_column='productName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    email = models.ForeignKey('Users', models.DO_NOTHING, db_column='email', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'need'


class Photos(models.Model):
    photoid = models.IntegerField(primary_key=True)
    photofile = models.ImageField(upload_to='main_app/img/',db_column='photoFile', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=60, blank=True, null=True)
    ownerid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'photos'


class Products(models.Model):
    pid = models.IntegerField(primary_key=True)
    pname = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    noofratings = models.IntegerField(db_column='noOfRatings', blank=True, null=True)  # Field name made lowercase.
    avgrating = models.FloatField(db_column='avgRating', blank=True, null=True)  # Field name made lowercase.
    owner = models.ForeignKey('Users', models.DO_NOTHING, db_column='owner', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class Renttransaction(models.Model):
    transid = models.IntegerField(db_column='transId', primary_key=True)  # Field name made lowercase.
    rentid = models.ForeignKey('Rentad', models.DO_NOTHING, db_column='rentid', blank=True, null=True)
    email = models.ForeignKey('Users', models.DO_NOTHING, db_column='email', blank=True, null=True)
    startdate = models.DateField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    starttime = models.TimeField(db_column='startTime', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='endDate', blank=True, null=True)  # Field name made lowercase.
    endtime = models.TimeField(db_column='endTime', blank=True, null=True)  # Field name made lowercase.
    rating = models.FloatField(blank=True, null=True)
    review = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rentTransaction'


class Rentad(models.Model):
    rentid = models.IntegerField(primary_key=True)
    pid = models.ForeignKey(Products, models.DO_NOTHING, db_column='pid', blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    adddate = models.DateField(db_column='addDate', blank=True, null=True)  # Field name made lowercase.
    expirydate = models.DateField(db_column='expiryDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'rentad'


class Sellad(models.Model):
    sellid = models.IntegerField(primary_key=True)
    pid = models.ForeignKey(Products, models.DO_NOTHING, db_column='pid', blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    adddate = models.DateField(db_column='addDate', blank=True, null=True)  # Field name made lowercase.
    expirydate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sellad'


class Users(models.Model):
    email = models.CharField(primary_key=True, max_length=40)
    name = models.CharField(max_length=50, blank=True, null=True)
    profilephoto = models.ImageField(upload_to='main_app/img/',db_column='profilePhoto', blank=True, null=True)  # Field name made lowercase.
    phnumber = models.CharField(db_column='phNumber', max_length=15, blank=True, null=True)  # Field name made lowercase.
    whnumber = models.CharField(db_column='whNumber', max_length=15, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Wishes(models.Model):
    email = models.ForeignKey(Users, models.DO_NOTHING, db_column='email', primary_key=True)
    pid = models.ForeignKey(Products, models.DO_NOTHING, db_column='pid')

    class Meta:
        managed = False
        db_table = 'wishes'
        unique_together = (('email', 'pid'),)
