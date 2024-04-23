from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone



# Create your models here.

class CarModel(models.Model):
    model = models.CharField(max_length=30,null=True)
    year = models.IntegerField(null=True)
    millage = models.IntegerField(null=True)
    tax = models.IntegerField(null=True)
    mpg = models.DecimalField(max_digits=10,decimal_places=1,null=True)
    engineSize = models.DecimalField(max_digits=3,decimal_places=1,null=True)
    transmission_automatic = models.IntegerField(null=True)
    transmission_manual = models.IntegerField(null=True)
    transmission_semi = models.IntegerField(null=True)
    fuel_diesel = models.IntegerField(null=True)
    fuel_electric = models.IntegerField(null=True)
    fuel_hybrid = models.IntegerField(null=True)
    fuel_other = models.IntegerField(null=True)
    fuel_petrol = models.IntegerField(null=True)
    

class Product_Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.category}'

class Product(models.Model):
    img_url = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=20,decimal_places=2)
    category = models.ForeignKey(Product_Category,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return f'{self.img_url} {self.name} {self.description} {self.price} {self.category}'
    
class LoanModel(models.Model):
    number_of_dependents = models.DecimalField(max_digits=20,decimal_places=2,null=True)
    anual_income = models.DecimalField(max_digits=20,decimal_places=2,null=True)
    loan_ammount = models.DecimalField(max_digits=20,decimal_places=2,null=True)
    loan_term = models.IntegerField(null=True)
    cibil_score = models.DecimalField(max_digits=20,decimal_places=2,null=True)
    residental_assets_value = models.DecimalField(max_digits=20,decimal_places=2,null=True)
    commercial_assets_value = models.DecimalField(max_digits=20,decimal_places=2,null=True)
    luxury_assets_value = models.DecimalField(max_digits=20,decimal_places=2,null=True)
    bank_asset_value = models.DecimalField(max_digits=20,decimal_places=2,null=True)
    graduate = models.IntegerField(null=True)
    employed = models.IntegerField(null=True)

    result = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.number_of_dependents} {self.anual_income} {self.loan_ammount} {self.loan_term} {self.cibil_score} {self.residental_assets_value} {self.commercial_assets_value} {self.luxury_assets_value} {self.bank_asset_value} {self.graduate} {self.employed} {self.result}  '


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    password = models.CharField(max_length=128,default='123')
    gender =models.CharField(max_length=1)
    sec_question = models.CharField(max_length=50)
    sec_answer= models.CharField(max_length=50)
    bank_info = models.OneToOneField(LoanModel, on_delete=models.CASCADE, null=True, blank=True)
    automobile_info = models.OneToOneField(CarModel, on_delete=models.CASCADE, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'surname', 'gender', 'sec_question', 'sec_answer', 'bank_info', 'automobile_info']

    def __str__(self):
        return self.username
    




    



