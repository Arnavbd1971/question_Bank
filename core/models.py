from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.admin.models import LogEntry


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault("is_user", True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

phone_regex = RegexValidator(regex='^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$',message='Invalid phone number')

class User(AbstractBaseUser, PermissionsMixin):
    idname = models.CharField(max_length=250, unique=True)
    display_name = models.CharField(max_length=250, blank=True)
    email = models.EmailField(max_length=250)
    phone = models.CharField(max_length=250, validators=[phone_regex], null=True, blank=True)
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'idname'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-is_active']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'



class Question(models.Model):
    question = models.TextField(null=False, blank=False, default='')
    option1 = models.TextField(null=False, blank=False, default='')
    option2 = models.TextField(null=False, blank=False, default='')
    option3 = models.TextField(null=False, blank=False, default='')
    option4 = models.TextField(null=False, blank=False, default='')
    option5 = models.TextField(null=False, blank=False, default='')
    answer = models.IntegerField(null=False, blank=False, default=0)
    explain = models.TextField(null=False, blank=False, default='')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        db_table = 'question'

class FavoriteQuestion(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='fav_question_user')
    question_id = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='fav_question_question')

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = 'FavoriteQuestion'
        verbose_name_plural = 'FavoriteQuestions'
        db_table = 'favorite_question'


class ReadQuestion(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='read_question_user')
    question_id = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='read_question_question')

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = 'ReadQuestion'
        verbose_name_plural = 'ReadQuestions'
        db_table = 'read_question'



