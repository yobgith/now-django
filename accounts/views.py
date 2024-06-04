from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #USER ACTIVATION 
            current_site = get_current_site(request)
            mail_subject = "Nous vous prions d'activer votre compte"
            message = render_to_string('accounts/account_verification_email.html', {
                "user": user,
                "domain":current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, "Merci de vous avoir inscrit chez nous. nous avons envoyé un e-mail de vérification à votre adresse e-mail [yobouet@gmail.com]. Vérifiez SV")
            return redirect('/accounts/login/?command=verification&email='+email)
    else:            
        form = RegistrationForm()
    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Vous être connectés. ')
            return redirect('dashboard')
        else:
            messages.error(request, 'Authentification invalide')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Vous êtes déconnectés')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Félicitation! Votre compte a été activé.")
        return redirect('login')
    else:
        messages.error(request, "Votre lien d'activation est Ivalide!")
        return redirect("register")


@login_required(login_url= 'login')    
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = "Réinitialisez votre Mot de Passe SVP"
            message = render_to_string('accounts/reset_password_email.html', {
                "user": user,
                "domain":current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "Un lien de réinitialisation vous a étés envoyé dans votre adresse mail")
            return redirect('login')

        else:
            messages.error(request, "Le compte n'existe pas!")
            return redirect("forgotPassword")
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Réinitialisez votre mot de passe SVP!')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Ce lien a expiré!')
        return redirect('login')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Votre mot de passe a bien été Réinitialisé')
            return redirect('login')
        else:
            messages.error(request, 'Les Mots de Passe ne Correspondent pas')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')