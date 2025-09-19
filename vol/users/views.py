from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404, render
from .forms import CustomUserCreationForm, TeamForm
from .models import CustomUser, Team
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.auth import get_user_model

def activateEmail(request, user, to_email):
    mail_subject = 'Подтвердите свой аккаунт'
    message = render_to_string('auth/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Уважаемый <b>{user}</b>, пожалуйста перейдите на свою почту <b>{to_email}</b> и нажмите \
           на отправленную ссылку на подтверждения почты. <b>Note:</b> Проверьте спам.')
    else:
        messages.error(request, f'Не удалось отправить сообщение на почту {to_email}, проверьте данные')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Спасибо за подтверждение, теперь вы можете войти в свой аккаунт')
        return redirect('signin')
    else:
        messages.error(request, 'Ссылка для активации недействительна')
    
    return redirect('games')

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if 'photo' in request.FILES:
                user.photo = request.FILES['photo']
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('games')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = CustomUserCreationForm()

    return render(
        request=request,
        template_name="auth/register.html",
        context={"form": form}
    )


class SignIn(LoginView):
    form_class = AuthenticationForm
    template_name = 'auth/login.html'

    def get_success_url(self):
        return reverse_lazy('games')


class Profile(DetailView):
    model = CustomUser
    template_name = 'auth/profile.html'
    context_object_name = 'user'
    slug_field = 'username'

def admin_check(user):
    return user.is_superuser

class UpdateRating(View):
    def get(self, request, slug):
        if not request.user.is_superuser and not request.user.status == 'B':
            return render(request, 'auth/error.html')  # or raise PermissionDenied

        user = get_object_or_404(CustomUser, username=slug)
        return render(request, 'auth/update_rating.html', {'user': user})
    
    def post(self, request, slug):
        if request.user.is_superuser or request.user.status == 'B':
            user = get_object_or_404(CustomUser, username=slug)
            new_rating = request.POST.get('rating')
            if new_rating is not None:
                user.rating = new_rating
                user.save()
            return redirect('profile', slug=slug)
        else:
            return render(request, 'auth/error.html')


def create_team(request):
    form = TeamForm()
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.team_rating = sum(form.cleaned_data['players'].values_list('rating', flat=True))
            team.save()
        else:
            form = TeamForm()
    return render(request, 'volleyball/teamform.html', {'form': form})



def TeamList(requeest):
    teams = Team.objects.all()
    return render(requeest, 'volleyball/teams.html', {'teams': teams})

def TeamDetail(request, *args, **kwargs):
    team = Team.objects.get(pk=kwargs['pk'])
    players = team.players.all()
    return render(request, 'volleyball/team_detail.html', {
        'team': team,
        'players': players,
        })