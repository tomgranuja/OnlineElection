#!/usr/bin/env python
"""Helper script for initial candidates load from csv file."""
import csv

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.contrib.auth.models import User

from votacion.chilean_RUN_utils import run_is_valid, run_clean
from votacion.models import Profile

# Convert csv table to row-dict list
def from_csv_table(fname):
    with open(fname, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        t = [row for row in reader]
        return t

class Command(BaseCommand):
    help = "Initial candidates load from csv file."

    def add_arguments(self, parser):
        parser.add_argument("filename")

    def handle(self, *args, **options):
        filename = options["filename"]
        try:
            raw_t = from_csv_table(filename)
        except FileNotFoundError:
            raise CommandError('File "%s" does not exist' % filename)

        self.stdout.write(
            self.style.SUCCESS(
                f"Read {len(raw_t)} entries"))
        t = [row for row in raw_t if run_is_valid(row['username'])]
        if len(t) < len(raw_t):
            [self.stdout.write(
                self.style.WARNING(
                    f"Skipping invalid RUN: {row.values()}"))
             for row in raw_t if row not in t]
        self.stdout.write(self.style.SUCCESS(f"Filtering to {len(t)} valid RUN entries"))
        for row in t:
            cleaned_run = run_clean(row["username"])
            user, created = User.objects.get_or_create(username=cleaned_run)
            if not created:
                self.stdout.write(
                    self.style.WARNING(
                        f"Updating preexisting user: {user.first_name}, {user.username}"))
            user.first_name = row["first_name"]
            user.last_name = row["last_name"]
            # user.email = row["email"]
            user.set_password(row["pass"])
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            if not created:
                self.stdout.write(
                    self.style.WARNING(
                        f"Updating preexisting profile: {profile.fullname()}"))
            profile.cell = row['cel']
            profile.save()
