from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

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


class EVENT(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    organiser_name = models.CharField(max_length=50, null=True, blank=True)
    organiser_email = models.EmailField(max_length=254)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.name


class TIME(models.Model):
    time = models.TimeField()

    def __str__(self):
        return str(self.time)


class EVENT_DATE(models.Model):
    event = models.ForeignKey(EVENT, on_delete=models.CASCADE, related_name='event', blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.date)


class ACCESS_POINT(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.name


class EVENT_SLOT(models.Model):
    time = models.ForeignKey(TIME, on_delete=models.CASCADE, blank=True, null=True)
    event_date = models.ForeignKey(EVENT_DATE, on_delete=models.CASCADE, related_name='event_date', blank=True,
                                   null=True)
    access_point = models.ForeignKey(ACCESS_POINT, on_delete=models.CASCADE, related_name='access_point', blank=True,
                                     null=True)

    def __str__(self):
        return str(self.event_date)


class SLOT_ACCESS_POINTS(models.Model):
    slot = models.ForeignKey(EVENT_SLOT, on_delete=models.CASCADE, related_name='slot', blank=True, null=True)
    access_point = models.ForeignKey(ACCESS_POINT, on_delete=models.CASCADE, related_name='accesspoint', blank=True,
                                     null=True)

    def __str__(self):
        return str(self.slot)

