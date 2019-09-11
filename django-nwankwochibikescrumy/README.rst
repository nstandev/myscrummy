=====
nwankwochibikescrumy
=====

nwankwochibikescrumy is a simple Django app.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "nwankwochibikescrumy" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'nwankwochibikescrumy',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('nwankwochibikescrumy/', include('nwankwochibikescrumy.urls')),

3. Run `python manage.py migrate` to create the nwankwochibikescrumy models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a nwankwochibikescrumy (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/nwankwochibikescrumy/ to use the app.