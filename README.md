# OnlineElection

OnlineElection is a small [python django](https://www.djangoproject.com/) site that allows registered users to vote for a candidate choosen among themselves.

This software takes numerous ideas from [CayumanDjango developed by ralamos](https://github.com/tomgranuja/CayumanDjango) and also is a good starting project to learn django.

## Install

### Install django in a python venv

Create [python venv](https://docs.python.org/3/library/venv.html), activate it and install django (needs python>=3.3 and python-venv):

```bash
$ mkdir ~/.venv
$ python -m venv ~/.venv/dj
$ source ~/.venv/dj/bin/activate

# No need --user because on a virtual env.
(dj)$ pip install django==5.1
(dj)$ python -m django --version
(dj)$ deactivate
```

The next time this environment is needed
use the activation script and then deactivate it to restore the system environment:

```bash
$ source ~/.venv/dj/bin/activate
(dj)$ ...
(dj)$ ...
(dj)$ deactivate
$ 
```

### Download github source code

Download the application source code.

```bash
# Clone repo
(dj)$ git clone https://github.com/tomgranuja/OnlineElection.git
```

## Test

Create the [django default database](https://docs.djangoproject.com/en/5.1/intro/tutorial02/#database-setup) and make an [admin user](https://docs.djangoproject.com/en/5.1/intro/tutorial02/#creating-an-admin-user):


```bash
# Make system database
(dj)$ cd OnlineElection
(dj) OnlineElection$ python manage.py migrate

# Create admin user
(dj) OnlineElection$ python manage.py createsuperuser
> Username: some-test-user
> Email address: admin@example.com
> Password: **********
> Password (again): *********
> Superuser created successfully.
```

The application server now is ready to run, but only the administrator user is registered.

To add new users run the server and go to the admin site [http://127.0.0.1:8000/admin]().

```bash
# Run the server
(dj) OnlineElection$ python manage.py runserver

# Go to http://127.0.0.1:8000/admin
```

Navigate to Users to add new users. Users that need to vote must use a chilean RUN as username (12345678-5). Then navigate to Profile to add new profiles for each user. This allow users to vote.

Finally, click at logout and navigate to site index [http://127.0.0.1:8000]() to authenticate as a regular user and vote.

## Initial candidates load from csv file

In order to import candidates from a local csv file, `import_from.py` management script is proportionated:

```bash
(dj) OnlineElection$ python manage.py import_from CSV_FILE
```

See the example csv file below:

```csv
username,first_name,last_name,cel,pass
1234567-4,John,Dowe,+569 8888 88 88,johnpass*
22987654-6,Peter,Parker,,peterpass*
```

## Local vars and secrets

Some local vars can be customize in `eleccion/.local_settings` file. This file should be created with chmod 600 filesystem permission to keep secrets.

``` bash
# Optional configuration vars
$ cd OnlineElection
$ touch eleccion/.local_settings
$ chmod 600 eleccion/.local_settings
```

### Secret key

The [secret key](https://docs.djangoproject.com/en/5.1/ref/settings/#secret-key) is used to provide cryptographic signing, and should be set to a unique, unpredictable value. In particular is used for sessions and messages.

The secret key must be a random 50 character minimum string. Use the following command to generate a secure string, see [generate-django-secret-key by Humberto Rocha](https://humberto.io/blog/tldr-generate-django-secret-key/).

```bash
$ python -c "import secrets; print(secrets.token_urlsafe(38))"
```

### Time zone

See [Time zones](https://docs.djangoproject.com/en/5.1/topics/i18n/timezones/) for an explanation of the time zone settings needed. In brief when time zone support is enabled, django stores UTC datetime data in the database, use time zone aware objects internally and translate them to the end user time zone in templates and forms.

Available time zones can be consulted in python with `zoneinfo.available_timezones()`

### Local settings example

This is an example `eleccion/.local_settings` file with a secret key and a chilean time zone.

```bash
SECRET_KEY = M1ikEok2WtfOatyf7xAaLHO-BsL1OlSVNpMpSX_kMZyajVhEZDI
TIME_ZONE = America/Santiago
```

