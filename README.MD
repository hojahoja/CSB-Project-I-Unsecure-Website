# Cyber Security Base Project I

https://cybersecuritybase.mooc.fi/module-3.1

## Installation instructions

Clone the repository. Make sure that you have the packages listed in the
requirements.txt installed through pip. If you want you can use a virtual
environment to separate the packages from your global setup. Use these commands
inside the project root directory.

Create the virtual environment.

```sh
python3 -m venv .venv
```

Activate the virtual environment inside the terminal.

On Linux:

```sh
source .venv/bin/activate
```

On Windows:

```sh
venv\Scripts\activate
```

Install the packages with:

```sh
pip install -r requirements.txt
```

Even if you don’t have pip the venv will have it pre-installed. You can exit the
virtual environment with the `deactivate` command.

Run the website from the project root directory with the command:

```sh
python3 manage.py runserver
```

The website should be accessible on localhost:8000 by default.

There are two working user accounts to test things out with.

Username: admin \
Password: 123

Username PollEnjoyer \
Password: fearmemortals

## The Project

This project uses the polls app introduced in the
[Django tutorial](https://docs.djangoproject.com/en/3.1/intro/tutorial01/) as a
basis. The polls page requires a login. Interacting, viewing and voting on polls
are solely reserved for logged-in users. Additionally, a rather unsecured
guestbook page has been implemented that allows attackers to do some undesirable
things. The guestbook does not require a login. This assignment uses the
[OWASP 2017 top 10](https://owasp.org/www-project-top-ten/2017/Top_10) list
which treats injection and xss-attacks as separate entries. The instructions
that tell you to edit specific lines refer to the lines as they are on Git Hub
if some lines are edited before the fix. Then the instructions might not lead to
be exact. It’s best to always refer to the line numbers on Git Hub rather than
your editor.

### FLAW 1: Guestbook filter form vulnerable to SQL Injection

[A1:2017 Injection](https://owasp.org/www-project-top-ten/2017/A1_2017-Injection)

Source code:
[views.py line 66](https://github.com/hojahoja/CSB-Project-I-Unsecure-Website/blob/41c132ed53929997d1ecedce515f14c68ec44b92/polls/views.py#L66)

The guestbook page has an option to filter users user by their username. The
problem with this filtering feature is that it uses a raw SQL query and takes
the input from the filter field directly as a where “argument”. This has been
implemented with an f-string allowing users to write direct SQL queries beyond
just the intended use. The method contains two commented-out lines of code that
change the SQL query into a parametrized query. To implement the fix replace
line 70 with line 68 and replace line 75 with line 73 in views.py. Now the
string from the filter field will be used as a parameter and will not be
executed by the DB sanitizing the input. You can test this by writing this in
the filter form: `' UNION select username, password from auth_user--`

### FLAW 2: Name and Message fields vulnerable to XSS

[A7:2017 Cross-Site Scripting](<https://owasp.org/www-project-top-ten/2017/A7_2017-Cross-Site_Scripting_(XSS)>)

Source code:
[guestbook.html line 9](https://github.com/hojahoja/CSB-Project-I-Unsecure-Website/blob/41c132ed53929997d1ecedce515f14c68ec44b92/polls/templates/polls/guestbook.html#L9)

The form fields in the guestbook page do not sanitize (escape) inputs so anyone
can write direct javascript code inside script tags into the text field and the
javascript code will be executed when the page is loaded. To fix this remove the
lines with autoscape off(line 9) and endautoescape(54). This will restore
Django’s default templating behavior. Now the code will render on the page as
regular text because special characters are escaped automatically and won’t be
treated as code by the browser. The database included with the repo has a couple
of example scripts included. The alert “u have been pwnd!” should stop popping
up after the fix has been implemented.

### FLAW 3: Individual poll pages can be accessed by manipulating the URL

[A5:2017 Broken Access Control](https://owasp.org/www-project-top-ten/2017/A5_2017-Broken_Access_Control)

Source code:
[urls.py line 12](https://github.com/hojahoja/CSB-Project-I-Unsecure-Website/blob/41c132ed53929997d1ecedce515f14c68ec44b92/polls/urls.py#L12)
And
[views.py line 33](https://github.com/hojahoja/CSB-Project-I-Unsecure-Website/blob/41c132ed53929997d1ecedce515f14c68ec44b92/polls/views.py#L33)

As mentioned in the introduction. The polls page is intended for logged-in users
only. When you enter the polls list page `/polls/` you are asked to log in.
However, while the poll view page requires a login, you can still access
individual poll pages for example `polls/1` or `polls/1/results`. If you know
the URL bypassing the intended access control. To fix this replace 12 with line
13 and replace line 14 with line 15 in urls.py. Additionally, uncomment the
`login_required` decorator on line 32 in views.py. Now every intended page
requires a login by the back end and the user cannot bypass the initial login
check by just adjusting the URL and skipping directly to a linked poll.

### FLAW 4: Django debug mode is active giving too much information

[A6:2017-Security Misconfiguration](https://owasp.org/www-project-top-ten/2017/A6_2017-Security_Misconfiguration)

Source code:
[settings.py line 27](https://github.com/hojahoja/CSB-Project-I-Unsecure-Website/blob/41c132ed53929997d1ecedce515f14c68ec44b92/CSBHarjoitus/settings.py#L27)

The OWASP lists “too informative Error handling” as a potential security issue.
The Django app has debug mode turned on and the error pages list quite a bit of
extra information. For example, it lists some paths exactly and you can see that
the number parameters are database id’s. Giving the user easy access to a lot of
detail on the app structure is not something we want a potential to know and
exploit. The fix for this is simple. Turn off debug mode in the settings.py
file. Change line 27 to `DEBUG = False` and uncomment line 30:
`ALLOWED_HOSTS = [“localhost”]`. Normally you would use the URL for your
website, but localhost will suffice here. Now the website error pages behave as
you’d expect from a website instead of spilling a bunch of information a regular
user should not require.

### FLAW 5: Filter and Message Forms do not require CSRF tokens

[Cross-Site Request Forgery (CSRF)](https://owasp.org/www-community/attacks/csrf)

Source code:
[guestbook.html line 26](https://github.com/hojahoja/CSB-Project-I-Unsecure-Website/blob/41c132ed53929997d1ecedce515f14c68ec44b92/polls/templates/polls/guestbook.html#L26)
And
[views.py line 52](https://github.com/hojahoja/CSB-Project-I-Unsecure-Website/blob/41c132ed53929997d1ecedce515f14c68ec44b92/polls/views.py#L52)

As stated in the assignment this is not listed in OWASP top 10 2017, but was an
allowed demonstration for this task. The guestbook page on this website does not
require or provide CSRF tokens for the forms within. Because of this, an
attacker could exploit the specific “action” link in their website, by creating
a malicious interactable object that would make a request to the form on this
guestbook page, but with their malicious functionality. Django provides the CSRF
token middleware which would normally block these kinds of malicious cross-site
requests. To fix this issue delete every `@csrf_exempt` decorator in the
views.py file (lines 52, 58, and 65). Now the forms in the guestbook page should
give you a 403 error page because of missing CSRF tokens. Enable the tokens on
the guestbook page by deleting the HTML comment (\<!---->) lines surrounding the
tokens (delete lines 25, 27, 38, and 40). Now the forms should work again with
CSRF protection enabled.
