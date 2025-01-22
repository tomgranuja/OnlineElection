from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
    '''Extend User by adding a cell and voted boolean field.'''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        )
    cell = models.CharField(
        "cell phone", max_length=30,
        blank=True,
        )
    is_candidate = models.BooleanField(
        "is candidate",
        default=False,
        )
    voted = models.BooleanField(
        "has voted",
        default=False,
        )
    
    def vote(self, name=None, null=False):
        '''Record a Vote instance and change Profile instance vote attrib to True.'''
        if self.voted:
            return
        if null:
            v = Vote(null=True)
        elif name is None:
            v = Vote()
        else:
            v = Vote.objects.vote_for_name(name)
        v.save()
        self.voted = True
        self.save()
        return v
    
    def username(self):
        return self.user.username
    
    def fullname(self):
        return self.user.get_full_name()
    
    # Better display in shell and admin site
    # Ej. <Profile: Alberto Carvajal>
    def __str__(self):
        return self.fullname()

class VoteManager(models.Manager):
    NON_CANDIDATE_KEY = {'blank_vote': 'Blancos', 'null_vote': 'Nulos'}
    
    def vote_for_name(self, name):
        p = Profile.objects.get(user__username = name)
        return self.model(candidate=p)
    
    def vote_count(self):
        count = {}
        for u in [v.candidate.username() for v in Vote.objects.all()
                  if not v.null and v.candidate is not None]:
            if u not in count:
                count[u] = 1
            else:
                count[u] += 1
        count = dict(sorted(count.items(), key=lambda t: t[1], reverse=True))
        # Add Blank votes entry
        blank_votes = len(Vote.objects.filter(candidate=None, null=False))
        count[self.NON_CANDIDATE_KEY['blank_vote']] = blank_votes
        # Add Null votes entry
        count[self.NON_CANDIDATE_KEY['null_vote']] = len(Vote.objects.filter(null=True))
        
        return count
    
    def vote_count_by_fullname(self):
        by_name = self.vote_count().items()
        count = {
            k if k in self.NON_CANDIDATE_KEY.values() else
            Profile.objects.get(user__username=k).fullname(): v
            for k,v in by_name
            }
        return count

class Vote(models.Model):
    '''Save an anonimous vote.'''
    candidate = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        )
    null = models.BooleanField(
        "null vote",
        default=False,
        )
    
    objects = VoteManager()
    # Better display in shell and admin site
    # Ej. <Vote: Alberto Carvajal>
    def __str__(self):
        if self.null:
            return 'Null vote'
        elif self.candidate is None:
            return 'Blank'
        return self.candidate.user.get_full_name()
    
class Election(models.Model):
    '''Election start, end and description.'''
    description = models.CharField(
        max_length=80,
        blank=True,
        )
    start = models.DateTimeField("election start")
    end = models.DateTimeField("election end")
    
    def is_in_the_past(self):
        return timezone.now() > self.end
    
    def is_in_the_future(self):
        return timezone.now() < self.start
    
    def is_active(self):
        if self.is_in_the_future():
            return False
        if self.is_in_the_past():
            return False
        return True
    
    def __str__(self):
        return self.start.date().isoformat()
