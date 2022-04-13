from django.db import models


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

