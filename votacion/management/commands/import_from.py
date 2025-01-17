#!/usr/bin/env python
"""Helper script for initial candidates load from csv file."""
import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from django.contrib.auth.models import User
from votacion.models import Profile

# Convert csv table to row-dict list
def from_csv_table(fname):
    with open(fname, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        t = [row for row in reader]
        return t

def rut_is_valid(rut):
    return True

class Command(BaseCommand):
    help = "Initial candidates load from csv file."

    def add_arguments(self, parser):
        parser.add_argument("filename")

    def handle(self, *args, **options):
        filename = options["filename"]
        try:
            t = from_csv_table(filename)
        except FileNotFoundError:
            raise CommandError('File "%s" does not exist' % filename)

        self.stdout.write(self.style.SUCCESS(f"Read {len(t)} entries"))
        t = [row for row in t if rut_is_valid(row['username'])]
        self.stdout.write(self.style.SUCCESS(f"Filtering to {len(t)} entries"))
        for row in t:
            user, created = User.objects.get_or_create(username=row["username"])
            if not created:
                self.stdout.write(self.style.WARNING(f"Updating preexisting user: {user.first_name}, {user.username}"))
            user.first_name = row["first_name"]
            user.last_name = row["last_name"]
            # user.email = row["email"]
            user.set_password(row["year"])
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            if not created:
                self.stdout.write(self.style.WARNING(f"Updating preexisting profile: {profile.fullname()}"))
            profile.cell = row['cel']
            profile.save()

