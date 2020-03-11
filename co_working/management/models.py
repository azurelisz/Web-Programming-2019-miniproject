from django.db import models
# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)

class Member(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length=30)
    money = models.IntegerField()

class Zone(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    price = models.IntegerField()
    available_seat = models.IntegerField()

class SeatBooking(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    time_check_in = models.DateTimeField(auto_now=True)
    time_check_out = models.DateTimeField(auto_now=True)
    total_price = models.IntegerField()
    create_date = models.DateField(auto_now=True)
    create_by = models.ForeignKey(User, on_delete=models.PROTECT)

class TopupLog(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.IntegerField()
    topup_date = models.DateTimeField(auto_now=True)
    topup_by = models.ForeignKey(User, on_delete=models.CASCADE)
