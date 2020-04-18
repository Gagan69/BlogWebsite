from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post




# HTML Pages

def home(request):
        return render(request, 'home/home.html')
    #return HttpResponse('This is home')

def about(request):

       
        return render(request,'home/about.html')


def contact(request):
       
        if request.method=='POST':
                name = request.POST['name']
                email = request.POST['email']
                phone = request.POST['phone']
                message = request.POST['message']

                if len(name)<2 or len(email)<3 or len(phone)<10 :
                        messages.error(request,"Please Fill the form correctly!")
                else:
                        contact = Contact(name=name, email=email, phone=phone, message=message)
                        contact.save()
                        messages.success(request,'Your message has been successfully sent!')

        return render(request,'home/contact.html')


def search(request):
        query = request.GET['query']
        if len(query)>78:
                allposts= Post.objects.none()
        else:
                allpostsTitle = Post.objects.filter(title__icontains=query)
                allpostsContent = Post.objects.filter(content__icontains=query)
                allposts = allpostsTitle.union(allpostsContent)
       
        if allposts.count() == 0:
                messages.warning(request,"No search results found. Please try different keywords")
               
        params={'allposts': allposts, 'query':query}
        return render(request, 'home/search.html',params)



#athentication APIs

def CreateSignUp(request):
        if request.method == 'POST':
                #get the post parameters
                username = request.POST['username']
                fname = request.POST['firstname']
                lname = request.POST['lastname']
                email = request.POST['email']
                password = request.POST['password']
                cpass = request.POST['cpassword']

                #check for errorneous inputs
                #username should be under 10 characters
                if len(username) > 10:
                        messages.error(request, 'Username must be under 10 characters.')
                        return redirect('home')

                #username should not be alphanumeric
                if not username.isalnum():
                        messages.error(request, 'Username should only contain letters and numbers.')
                        return redirect('home')

                #password should match
                if password != cpass:
                        messages.error(request, 'Password mis-match.')
                        return redirect('home')


                #create the user
                myuser = User.objects.create_user(username, email, password)
                myuser.first_name = fname       
                myuser.last_name = lname
                myuser.save()
                messages.success(request, 'User has been successfully created')
                return redirect('home')

        else:
                return HttpResponse('404 - Not Found!')


def handleLogin(request):
        if request.method =='POST':
                #get the post parameters
                loginusername=request.POST['loginusername']
                loginpassword = request.POST['loginpassword']

                user = authenticate(username=loginusername,  password=loginpassword)

                if user is not None:
                        login(request, user)
                        messages.success(request,'Successfully Logged In')
                        return redirect('home')
                else:
                        messages.error(request,'Invalid Username/Password. Please try again ')
                        return redirect('home')

        return HttpResponse('404 - Not Found')



def handleLogout(request):
        logout(request)
        messages.success(request, "Successfully Logged Out")
        return redirect('home')
       



