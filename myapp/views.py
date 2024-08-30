from django.shortcuts import render,redirect
from .models import Contact,User,Property,Inquiry
from django.conf import settings
from django.core.mail import send_mail
import random
# Create your views here.
def index(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			return render(request,'index.html')
		elif user.usertype=='seller':
			return render(request,'seller_index.html')
		elif user.usertype=='admin':
			sellers=User.objects.filter(usertype="seller")
			users=User.objects.filter(usertype="user")
			properties=Property.objects.all()
			total_property=len(properties)
			total_sellers=len(sellers)
			total_buyers=len(users)
			all_buyers=User.objects.all()
			total_user=len(all_buyers)
			return render(request,'admin_index.html',{'all_buyers':all_buyers,'total_user':total_user,'total_sellers':total_sellers,'total_buyers':total_buyers,'total_property':total_property})

		else:
			return redirect('logout')	
	except:
		return render(request,'index.html')

def seller_index(request):
	return render(request,'seller_index.html')

def contact(request):
	if request.method=="POST":
		print("Post called")
		Contact.objects.create(
				fname=request.POST['fname'],
				lname=request.POST['lname'],
				email=request.POST['email'],
				message=request.POST['message']
			)
		msg="Contact Saved Successfully"
		return render(request,'contact.html',{'msg':msg})
	else:
		return render(request,'contact.html')

def signup(request):
	if request.method=="POST":
		try:
			user=User.objects.get(
					email=request.POST['email'],
					password=request.POST['password']
				)
			msg="Email Already Registered"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						password=request.POST['password'],
						cpassword=request.POST['cpassword'],
						address=request.POST['address'],
						usertype=request.POST['usertype'],
						image=request.FILES['image'],
					)
				msg="User Sign Up Successfully!!Go To Your Registered Email Id For OTP."
				user=User.objects.get(email=request.POST['email'])
				subject = 'OTP For Forgot Password'
				otp=random.randint(1000,9999)
				message = 'OTP For Login Is : '+str(otp)
				email_from = settings.EMAIL_HOST_USER
				recipient_list = [user.email, ]
				send_mail( subject, message, email_from, recipient_list )
				return render(request,'verify_email_otp.html',{'msg':msg,'email':user.email,'otp':otp})
			else:
				msg="Password & Confirm Password Does Not Matched"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(
					email=request.POST['email'],
					password=request.POST['password']
				)
			if user.usertype=="user":

				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['image']=user.image.url
				return render(request,'index.html')

			elif user.usertype=="seller":
				inq=[]
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['image']=user.image.url
				inquiries=Inquiry.objects.all()
				for i in inquiries:
					if i.property.property_seller==user:
						inq.append(i)
				request.session['inquiry']=len(inq)
				return render(request,'seller_index.html')
			
			elif user.usertype=="admin":
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['image']=user.image.url
				sellers=User.objects.filter(usertype="seller")
				users=User.objects.filter(usertype="user")
				properties=Property.objects.all()
				total_property=len(properties)
				total_sellers=len(sellers)
				total_buyers=len(users)
				all_buyers=User.objects.all()
				all_buyers=Contact.objects.all()
				total_user=len(all_buyers)
				users=User.objects.filter(admin_status=False,usertype="seller")
				request.session['unverified_user']=len(users)
				return render(request,'admin_index.html',{'all_buyers':all_buyers,'total_user':total_user,'total_sellers':total_sellers,'total_buyers':total_buyers,'total_property':total_property})
			else:
				pass
		except Exception as e:
			print("Error : ",e)
			msg="Email Or Password Is Incorrect"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['image']
		return render(request,'login.html')
	except:
		return render(request,'login.html')

def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.cpassword=request.POST['new_password']
				user.save()
				return redirect('logout')
			else:
				msg="New Password & Confirm New Password Does Not Matched"
				return render(request,'change_password.html',{'msg':msg})
		else:
			msg="Old Password Is Incorrect"
			return render(request,'change_password.html',{'msg':msg})

	else:
		return render(request,'change_password.html')

def seller_change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.cpassword=request.POST['new_password']
				user.save()
				return redirect('logout')
			else:
				msg="New Password & Confirm New Password Does Not Matched"
				return render(request,'seller_change_password.html',{'msg':msg})
		else:
			msg="Old Password Is Incorrect"
			return render(request,'seller_change_password.html',{'msg':msg})

	else:
		return render(request,'seller_change_password.html')

def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			subject = 'OTP For Forgot Password'
			otp=random.randint(1000,9999)
			message = 'OTP For Forgot Password Is : '+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'otp.html',{'email':user.email,'otp':otp})
		except:
			msg="Email Id Not Registered"
			return render(request,'forgot_password.html',{'msg':msg})	
	else:
		return render(request,'forgot_password.html')

def verify_otp(request):
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	email=request.POST['email']

	if otp==uotp:
		return render(request,'new_password.html',{'email':email})
	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'email':email,'otp':otp,'msg':msg})

def verify_email_otp(request):
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	email=request.POST['email']

	if otp==uotp:
		user=User.objects.get(email=email)
		user.verfied=True
		user.save()
		msg="User Verified Successfully"
		return render(request,'login.html',{'msg':msg})
	else:
		msg="Invalid OTP"
		return render(request,'verify_email_otp.html',{'email':email,'otp':otp,'msg':msg})

def new_password(request):
	email=request.POST['email']
	new_password=request.POST['new_password']
	cnew_password=request.POST['cnew_password']

	if new_password==cnew_password:
		user=User.objects.get(email=email)
		user.password=new_password
		user.cpassword=new_password
		user.save()
		msg="Password Updated Successfully"
		return render(request,'login.html',{'msg':msg})
	else:
		msg="Password & Confirm Password Does Not Matched"
		return render(request,'new_password.html',{'email':email,'msg':msg})

def seller_add_property(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		Property.objects.create(
				property_seller=user,
				property_type=request.POST['property_type'],
				property_sub_type=request.POST['property_sub_type'],
				property_location=request.POST['property_location'],
				property_area=request.POST['property_area'],
				property_price=request.POST['property_price'],
				property_address=request.POST['property_address'],
				property_image1=request.FILES['property_image1'],
				property_image2=request.FILES['property_image2'],
				property_image3=request.FILES['property_image3'],
				property_image4=request.FILES['property_image4'],
				property_image5=request.FILES['property_image5']
			)
		msg="Property Added Successfully"
		return render(request,'seller_add_property.html',{'msg':msg})
	else:
		return render(request,'seller_add_property.html')

def seller_view_property(request):
	user=User.objects.get(email=request.session['email'])
	properties=Property.objects.filter(property_seller=user)
	return render(request,'seller_view_property.html',{'properties':properties})

def seller_property_detail(request,pk):
	property=Property.objects.get(pk=pk)
	return render(request,'seller_property_detail.html',{'property':property})

def seller_edit_property(request,pk):
	property=Property.objects.get(pk=pk)
	if request.method=="POST":
		property.property_area=request.POST['property_area']
		property.property_price=request.POST['property_price']
		property.property_address=request.POST['property_address']
		try:
			property.property_image1=request.FILES['property_image1']
		except:
			pass

		try:
			property.property_image2=request.FILES['property_image2']
		except:
			pass

		try:
			property.property_image3=request.FILES['property_image3']
		except:
			pass

		try:
			property.property_image4=request.FILES['property_image4']
		except:
			pass

		try:
			property.property_image5=request.FILES['property_image5']
		except:
			pass
		property.save()
		return redirect('seller_view_property')
	else:
		return render(request,'seller_edit_property.html',{'property':property})

def seller_delete_property(request,pk):
	property=Property.objects.get(pk=pk)
	property.delete()
	return redirect('seller_view_property')

def admin_index(request):
	sellers=User.objects.filter(usertype="seller")
	users=User.objects.filter(usertype="user")
	properties=Property.objects.all()
	total_property=len(properties)
	total_sellers=len(sellers)
	total_buyers=len(users)
	all_buyers=User.objects.all()
	total_user=len(all_buyers)
	return render(request,'admin_index.html',{'all_buyers':all_buyers,'total_user':total_user,'total_sellers':total_sellers,'total_buyers':total_buyers,'total_property':total_property})

def admin_all_buyers(request):
	all_buyers=User.objects.filter(usertype='user')
	return render(request,'admin_all_buyers.html',{'all_buyers':all_buyers})

def admin_all_sellers(request):
	all_buyers=User.objects.filter(usertype='seller')
	return render(request,'admin_all_sellers.html',{'all_buyers':all_buyers})

def unverified_user(request):
	users=User.objects.filter(admin_status=False,usertype="seller")
	request.session['unverified_user']=len(users)
	return render(request,'admin_unverified_user.html',{'users':users})	

def admin_edit_profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		#user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		#user.usertype=request.POST['usertype']
		try:
			user.image=request.FILES['image']
		except:
			pass
		user.save()
		request.session['image']=user.image.url
		msg="Profile Updated Successfully"
		return render(request,'admin_edit_profile.html',{'user':user,'msg':msg})
	else:
		return render(request,'admin_edit_profile.html',{'user':user})

def seller_edit_profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		user.usertype=request.POST['usertype']
		try:
			user.image=request.FILES['image']
		except:
			pass
		user.save()
		request.session['image']=user.image.url
		msg="Profile Updated Successfully"
		return render(request,'seller_edit_profile.html',{'user':user,'msg':msg})
	else:
		return render(request,'seller_edit_profile.html',{'user':user})

def admin_all_properties(request):
	all_properties=Property.objects.all()
	return render(request,'admin_all_properties.html',{'all_properties':all_properties})

def admin_property_detail(request,pk):
	property=Property.objects.get(pk=pk)
	print(property)
	return render(request,'admin_property_detail.html',{'property':property})

def admin_verify_seller(request,pk):
	user=User.objects.get(pk=pk)
	user.admin_status=True
	user.save()
	return redirect('unverified_user')

def admin_reject_seller(request,pk):
#	user=User.objects.get(pk=pk)
#	user.admin_status=False
#	user.delete()
#	user.save()
#	return redirect('unverified_user')
	user=User.objects.get(pk=pk)
	user.admin_status=False
	user.delete()
	sellers=User.objects.filter(usertype="seller")
	user=User.objects.filter(usertype="user")
	properties=Property.objects.all()
	total_property=len(properties)
	total_sellers=len(sellers)
	total_buyers=len(user)
	all_buyers=User.objects.all()
	total_user=len(all_buyers)
	return render(request,'admin_index.html',{'all_buyers':all_buyers,'total_user':total_user,'total_sellers':total_sellers,'total_buyers':total_buyers,'total_property':total_property})

def admin_edit_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.cpassword=request.POST['new_password']
				user.save()
				return redirect('logout')
			else:
				msg="New Password & Confirm New Password Does Not Matched"
				return render(request,'admin_edit_password.html',{'msg':msg})
		else:
			msg="Old Password Is Incorrect"
			return render(request,'admin_edit_password.html',{'msg':msg})

	else:
		return render(request,'admin_edit_password.html')

def admin_delete_user(request,pk):
	user=User.objects.get(pk=pk)
	user.delete()
	msg="User Deleted Successfully"
	sellers=User.objects.filter(usertype="seller")
	users=User.objects.filter(usertype="user")
	properties=Property.objects.all()
	total_property=len(properties)
	total_sellers=len(sellers)
	total_buyers=len(users)
	all_buyers=User.objects.all()
	total_user=len(all_buyers)
	return render(request,'admin_index.html',{'all_buyers':all_buyers,'total_user':total_user,'total_sellers':total_sellers,'total_buyers':total_buyers,'total_property':total_property,'msg':msg})

def properties(request):
	return render(request,'properties.html')

def tenaments(request):
	tenaments=Property.objects.filter(property_type='Tenament')
	return render(request,'tenaments.html',{'tenaments':tenaments})

def flat(request):
	flats=Property.objects.filter(property_type='Flat')
	return render(request,'flats.html',{'flats':flats})

def property_details(request,pk):
	inquiry_flag=False
	try:
		
		buyer=User.objects.get(email=request.session['email'])
		property=Property.objects.get(pk=pk)
		try:
			Inquiry.objects.get(buyer=buyer,property=property)
			inquiry_flag=True
		except Exception as e:
			print(e)
		print(inquiry_flag)
		return render(request,'property_details.html',{'property':property,'inquiry_flag':inquiry_flag})
	except:
		msg="Please Login For Proceed"
		return render(request,'login.html',{'msg':msg})

def property_inquiry(request,pk):
	property=Property.objects.get(pk=pk)
	buyer=User.objects.get(email=request.session['email'])
	Inquiry.objects.create(buyer=buyer,property=property)
	subject = 'Inquiry Related To Your Property At Dream Property'
	message = 'Hello Owner, Your Property Get Inquired At Our Site.\n Please Find The Buyers Detail Below.\nBuyer Name : '+str(buyer.fname)+"\nBuyer Email : "+str(buyer.email)+"\nBuyer Contact Number : "+str(buyer.mobile)
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [property.property_seller.email, ]
	send_mail( subject, message, email_from, recipient_list)
	msg="Inquiry Sent"
	return render(request,'properties.html',{'msg':msg})

def search(request):
	if request.method=="POST":
		search=request.POST['search']
		properties=Property.objects.filter(property_type__contains=search)
		return render(request,'search.html',{'properties':properties})
	else:
		return render(request,'search.html')

def seller_notification(request):
	user=User.objects.get(email=request.session['email'])
	inquiries=Inquiry.objects.all()
	inq=[]
	for i in inquiries:
		if i.property.property_seller==user:
			inq.append(i)
	print(inq)
	return render(request,'seller_notification.html',{'inq':inq})

def property_details_flats(request,pk):
	inquiry_flag=False
	try:

		buyer=User.objects.get(email=request.session['email'])
		property=Property.objects.get(pk=pk)
		try:
			Inquiry.objects.get(buyer=buyer,property=property)
			inquiry_flag=True
		except Exception as e:
			print(e)
		print(inquiry_flag)
		return render(request,'property_details_flat.html',{'property':property,'inquiry_flag':inquiry_flag})
	except:
		msg="Please Login For Proceed"
		return render(request,'login.html',{'msg':msg})

def property_inquiry_flats(request,pk):
	property=Property.objects.get(pk=pk)
	buyer=User.objects.get(email=request.session['email'])
	Inquiry.objects.create(buyer=buyer,property=property)
	subject = 'Inquiry Related To Your Property At Dream Property'
	message = 'Hello Owner, Your Property Get Inquired At Our Site.\n Please Find The Buyers Detail Below.\nBuyer Name : '+str(buyer.fname)+"\nBuyer Email : "+str(buyer.email)+"\nBuyer Contact Number : "+str(buyer.mobile)
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [property.property_seller.email, ]
	send_mail( subject, message, email_from, recipient_list)
	msg="Inquiry Sent"
	return render(request,'properties.html',{'msg':msg})

def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		#user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		#user.usertype=request.POST['usertype']
		try:
			user.image=request.FILES['image']
		except:
			pass
		user.save()
		request.session['image']=user.image.url
		msg="Profile Updated Successfully"
		return render(request,'profile.html',{'user':user,'msg':msg})
	else:
		return render(request,'profile.html',{'user':user})

def admin_deals_flats(request):
	return render(request,'admin_deals_flats.html')

def admin_deals_villas(request):
	return render(request,'admin_deals_villas.html')

def admin_deals_bungalow(request):
	return render(request,'admin_deals_bungalow.html')

def admin_deals_tenament(request):
	return render(request,'admin_deals_tenament.html')

def seller_property_sell(request,pk):
	inquiry=Inquiry.objects.get(pk=pk)
	property=Property.objects.get(pk=inquiry.property.pk)
	property.status=True
	property.save()
	inquiry.status=True
	inquiry.save()
	return redirect('seller_notification')

def bungalow(request):
	bungalow=Property.objects.filter(property_type='Bungalow')
	return render(request,'bungalow.html',{'bungalow':bungalow})

def property_details_bungalow(request,pk):
	inquiry_flag=False
	try:
		buyer=User.objects.get(email=request.session['email'])
		property=Property.objects.get(pk=pk)
		try:
			Inquiry.objects.get(buyer=buyer,property=property)
			inquiry_flag=True
		except Exception as e:
			print(e)
		print(inquiry_flag)
		return render(request,'property_details_bungalow.html',{'property':property,'inquiry_flag':inquiry_flag})
	except:
		msg="Please Login For Proceed"
		return render(request,'login.html',{'msg':msg})

def property_inquiry_bungalow(request,pk):
	property=Property.objects.get(pk=pk)
	buyer=User.objects.get(email=request.session['email'])
	Inquiry.objects.create(buyer=buyer,property=property)
	subject = 'Inquiry Related To Your Property At Dream Property'
	message = 'Hello Owner, Your Property Get Inquired At Our Site.\n Please Find The Buyers Detail Below.\nBuyer Name : '+str(buyer.fname)+"\nBuyer Email : "+str(buyer.email)+"\nBuyer Contact Number : "+str(buyer.mobile)
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [property.property_seller.email, ]
	send_mail( subject, message, email_from, recipient_list)
	msg="Inquiry Sent"
	return render(request,'properties.html',{'msg':msg})

def villas(request):
	villas=Property.objects.filter(property_type='Villas')
	return render(request,'villas.html',{'villas':villas})

def property_details_villas(request,pk):
	inquiry_flag=False
	try:

		buyer=User.objects.get(email=request.session['email'])
		property=Property.objects.get(pk=pk)
		try:
			Inquiry.objects.get(buyer=buyer,property=property)
			inquiry_flag=True
		except Exception as e:
			print(e)
		print(inquiry_flag)
		return render(request,'property_details_villas.html',{'property':property,'inquiry_flag':inquiry_flag})
	except:
		msg="Please Login For Proceed"
		return render(request,'login.html',{'msg':msg})

def property_inquiry_villas(request,pk):
	property=Property.objects.get(pk=pk)
	buyer=User.objects.get(email=request.session['email'])
	Inquiry.objects.create(buyer=buyer,property=property)
	subject = 'Inquiry Related To Your Property At Dream Property'
	message = 'Hello Owner, Your Property Get Inquired At Our Site.\n Please Find The Buyers Detail Below.\nBuyer Name : '+str(buyer.fname)+"\nBuyer Email : "+str(buyer.email)+"\nBuyer Contact Number : "+str(buyer.mobile)
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [property.property_seller.email, ]
	send_mail( subject, message, email_from, recipient_list)
	msg="Inquiry Sent"
	return render(request,'properties.html',{'msg':msg})

def total_feedbacks(request):
	all_buyers=Contact.objects.all()
	return render(request,'total_feedbacks.html',{'all_buyers':all_buyers})