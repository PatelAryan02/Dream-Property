from django.db import models
from django.utils import timezone

# Create your models here.
class Contact(models.Model):
	fname=models.CharField(max_length=100,default="")
	lname=models.CharField(max_length=100,default="")
	email=models.CharField(max_length=100)
	message=models.TextField()

	def __str__(self):
		return self.fname+"-"+self.lname

class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.IntegerField()
	password=models.CharField(max_length=100)
	cpassword=models.CharField(max_length=100)
	address=models.TextField()
	usertype=models.CharField(max_length=100)
	image=models.ImageField(upload_to="images/",null=True,blank=True)
	verfied=models.BooleanField(default=False)
	admin_status=models.BooleanField(default=False)

	def __str__(self):
		return self.fname+" - "+self.lname

class Property(models.Model):
	CHOICE1=(
			('Flat','Flat'),
			('Tenament','Tenament'),
			('Bungalow','Bungalow'),
			('villas','villas'),
		)
	CHOICE2=(
			('1 BHK','1 BHK'),
			('2 BHK','2 BHK'),
			('3 BHK','3 BHK'),
			('4 BHK','4 BHK'),
			('5 BHK','5 BHK'),
			('6 BHK','6 BHK'),
			('7 BHK','7 BHK'),
			('8 BHK','8 BHK'),

		)
	CHOICE3=(
			('Maninagar','Maninagar'),
			('Memnagar','Memnagar'),
			('Bopal','Bopal'),
			('Iskon','Iskon'),
			('Gota','Gota'),
			('Vaishnodevi','Vaishnodevi'),
			('Naranpura','Naranpura'),
			('Sola','Sola'),
			('Thaltej','Thaltej'),
			('Sarkej','Sarkej'),
			('Shilaj','Shilaj'),
			('Navrangpura','Navrangpura'),
			('Gurukul','Gurukul'),
			('Juhapura','Juhapura'),
			('Ambavadi','Ambavadi'),
			('Shivranjani','Shivranjani'),
			('Ghodasar','Ghodasar'),
			('Vastrapur','Vastrapur'),
			('Vastral','Vastral'),
			('K.K Nagar','K.K Nagar'),
		)
	property_seller=models.ForeignKey(User,on_delete=models.CASCADE)
	property_type=models.CharField(max_length=100,choices=CHOICE1)
	property_sub_type=models.CharField(max_length=100,choices=CHOICE2)
	property_location=models.CharField(max_length=100,choices=CHOICE3,default="Bopal")
	property_area=models.CharField(max_length=100)
	property_price=models.CharField(max_length=100)
	property_address=models.TextField()
	property_desc=models.TextField(default="")
	property_image1=models.ImageField(upload_to="images/")
	property_image2=models.ImageField(upload_to="images/")
	property_image3=models.ImageField(upload_to="images/")
	property_image4=models.ImageField(upload_to="images/")
	property_image5=models.ImageField(upload_to="images/")
	status=models.BooleanField(default=False)

	def __str__(self):
		return self.property_type

class Inquiry(models.Model):

	buyer=models.ForeignKey(User,on_delete=models.CASCADE,default="")
	property=models.ForeignKey(Property,on_delete=models.CASCADE,default="")
	inquiry_date=models.DateTimeField(default=timezone.now)
	status=models.BooleanField(default=False)

	def __str__(self):
		return self.buyer.fname+" - "+self.property.property_type