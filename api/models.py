from django.db import models

class Account(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    email = models.CharField(db_column='Email', unique=True, max_length=50)
    password = models.CharField(db_column='Password', max_length=50)
    name = models.CharField(db_column='Name', db_collation='utf8mb4_bin', max_length=50)

    class Meta:
        db_table = 'account'
        ordering = ['id']
        managed = False

    def __str__(self):
        return self.name
    
    def set_password(self, raw_password):
        self.password = raw_password

class Ticket(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    license = models.CharField(db_column='License', max_length=10) 
    timein = models.DateTimeField(db_column='TimeIn')
    timeout = models.DateTimeField(db_column='TimeOut', blank=True, null=True) 
    total = models.DecimalField(db_column='Total', max_digits=18, decimal_places=3, blank=True, null=True)  
    ispaid = models.IntegerField(db_column='IsPaid')  

    class Meta:
        ordering = ['id']
        db_table = 'ticket'
        managed = False
    
class ParkingLot(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    isfree = models.IntegerField(db_column='IsFree')

    class Meta:
        ordering = ['id']
        db_table = 'parkinglot'
        managed = False

    def change_status(self, isfree):
        self.isfree = not isfree