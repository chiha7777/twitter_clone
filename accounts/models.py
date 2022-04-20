from django.contrib.auth.models import User

class Employee(models.Model):
  user = models.OneToOneField(User, on delete=models.CASCADE)
  department = models.CharField(max_length=100)
