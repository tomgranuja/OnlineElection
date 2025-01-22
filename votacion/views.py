from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .forms import RunLoginForm
from .models import Election, Profile, Vote

# Create your views here.

class RunLoginView(LoginView):
    authentication_form = RunLoginForm
    template_name = 'registration/run_login.html'

def index_raw(request):
    block = (
"You're at the votacion index.<br>"
"Now is {}<br>"
"So Election.is_active: {}.<br>"
"And Election.is_in_the_future: {}.<br>"
"And Election.is_in_the_past: {}."
)
    e = Election.objects.last()
    s = block.format(
        timezone.now().isoformat(),
        e.is_active(),
        e.is_in_the_future(),
        e.is_in_the_past(),
        )
    return HttpResponse(s)

def candidatos(request):
    election = Election.objects.last()
    profiles = Profile.objects.filter(is_candidate=True)
    user_voted = { p.fullname(): p.voted for p in profiles }
    count = Vote.objects.vote_count_by_fullname()
    context = { 
        'election': election,
        'now_date': timezone.now(),
        'user_voted': user_voted,
        'count': count,
        }
    return render(request, 'votacion/candidatos.html', context)

@login_required
def vote(request):
    user = Profile.objects.get(user=request.user)
    election = Election.objects.last()
    if election.is_in_the_past():
        return HttpResponseRedirect(reverse("election_over"))
    if election.is_in_the_future():
        return HttpResponseRedirect(reverse("before_election"))
    if user.voted:
        return HttpResponseRedirect(reverse("already_voted"))
    if 'null' in request.POST:
        user.vote(null=True)
        return HttpResponseRedirect(reverse("vote_success"))
    elif 'candidate' in request.POST:
        if 'blank' in request.POST['candidate']:
            user.vote()
        else:
           user.vote(name=request.POST['candidate'])
        return HttpResponseRedirect(reverse("vote_success"))
    else:
        context = {'profiles': Profile.objects.filter(is_candidate=True),}
        return render(request, 'votacion/eleccion_candidato.html', context)

def vote_success(request):
    return render(request, 'votacion/vote_success.html')

def already_voted(request):
    return render(request, 'votacion/already_voted.html')

def before_election(request):
    context = {'election': Election.objects.last(),}
    return render(request, "votacion/before_election.html", context)

def election_over(request):
    count = Vote.objects.vote_count_by_fullname()
    context = {
        'election': Election.objects.last(),
        'count': count,
        }
    return render(request, "votacion/election_over.html", context)

