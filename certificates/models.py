from django.db import models

class Position(models.Model):
    name = models.TextField()
    external_code = models.TextField(null=True)

class Department(models.Model):
    name = models.TextField()
    external_code = models.TextField(null=True)

class PowerOfAttorney(models.Model):
    number = models.IntegerField()
    issue_date = models.DateField()
    expiration_date = models.DateField()

class Certificate(models.Model):
    serial_number = models.TextField()
    issue_date = models.DateField()
    expiration_date = models.DateField()
    issued_by = models.TextField()

class Employee(models.Model):
    last_name = models.TextField()
    first_name = models.TextField()
    middle_name = models.TextField(null=True)
    snils = models.TextField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    power_of_attorney = models.ForeignKey(PowerOfAttorney, on_delete=models.CASCADE)
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    certificate_expiration_date = models.DateField(null=True)
    is_terminated = models.BooleanField(default=False)
