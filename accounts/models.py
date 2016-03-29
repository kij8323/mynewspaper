#coding=utf-8
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# from article.models import Article
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class MyUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
        	raise ValueError('Must include username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
        	username = username,
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,  password):
        """
        Creates and saves a superuser with the given username, email and password.
        """

        user = self.create_user(
			username=username,
			email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#注册用户数据库
class MyUser(AbstractBaseUser):
	username = models.CharField(
	    max_length=255,
	    unique=True,
	)
	email = models.EmailField(
	    verbose_name='email address',
	    max_length=255,
	    #unique=True,
	)
	first_name = models.CharField(
			max_length=120,
			null=True,
			blank=True,
			)
	last_name = models.CharField(
			max_length=120,
			null=True,
			blank=True,
			)

	is_member = models.BooleanField(default=False, 
					verbose_name='Is Paid Member')
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	icon = models.ImageField(upload_to='images', null=True, blank=True, default='images/78avatarbig.jpg')
	#特殊查询功能
	objects = MyUserManager()
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	fakepassword = models.CharField(max_length=255,null=True, blank=True)
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']


	def __unicode__(self):
	    return self.username

	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.icon)

	def get_full_name(self):
	    # The user is identified by their email address
	    return "%s %s" %(self.first_name, self.last_name)

	def get_short_name(self):
	    # The user is identified by their email address
	    return self.first_name

	def has_perm(self, perm, obj=None):
	    "Does the user have a specific permission?"
	    # Simplest possible answer: Yes, always
	    return True

	def has_module_perms(self, app_label):
	    "Does the user have permissions to view the app `app_label`?"
	    # Simplest possible answer: Yes, always
	    return True

	def get_absolute_url(self):
		return reverse('user_detailinformations', kwargs={"user_id": self.id})
		
	@property
	def is_staff(self):
	    "Is the user a member of staff?"
	    # Simplest possible answer: All admins are staff
	    return self.is_admin

	# def get_absolute_url(self):
	# 	return reverse('home')


#用户信息数据库
class UserProfile(models.Model):
	user = models.OneToOneField(MyUser)
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	company_name = models.CharField(max_length=50, null=True, blank=True)
	profession = models.CharField(max_length=20, null=True, blank=True)
	qq_address = models.CharField(max_length=20, null=True, blank=True)
	weixin_address = models.CharField(max_length=20, null=True, blank=True)
	my_introduction = models.CharField(max_length=30, null=True, blank=True)
	def __unicode__(self):
		return self.user.username
	def get_image_url(self):
		return "%s%s" %(settings.STATIC_URL, self.image)


# class MyUserEmailForm(ModelForm):
#     class Meta:
#         model = MyUser
#         fields = ['email']
#         labels = {
#         'email': _('邮箱地址'),
#     	}


class MyUserIconForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['icon']

# class MyUserPassWForm(ModelForm):
#     class Meta:
#         model = MyUser
#         fields = ['fakepassword']

