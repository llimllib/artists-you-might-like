Handling site media (staticfiles)
=================================

_note: In the spirit of helping, this is how I would rewrite the staticfiles section of your docs.  I disclaim all copyright, so if you'd like to use it, please do._

Gondor can optionally handle your static media for you. To enable static media handling, first go to your .gondor file and enable staticfiles:

    [app]
    staticfiles = on

In order for Gondor to host your files, you must use either _[django.contrib.staticfiles](https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/)_ or _[django-staticfiles](http://pypi.python.org/pypi/django-staticfiles/)_ in your application to host static files. Make sure that one of the two is included in your checked-in settings file so that Gondor knows where to find your static files.

Once you have a staticfiles app set up and running, you should be able to run this command to verify that it's able to find your static media:

    ./manage.py collectstatic

When you upload your application with static files to Gondor, the server will take care of setting up your *_ROOT_ and *_URL_ settings, changing them to these values:

    MEDIA_ROOT = "<generated>"
    STATIC_ROOT = "<generated>"
    MEDIA_URL = "/site_media/media/"
    STATIC_URL = "/site_media/static/"
    ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

If you do not wish to use Gondor's static file hosting, you must set your MEDIA_URL and STATIC_URL settings to an absolute URL (e.g. http://cdn.example.com/something/).

Finally, you should ensure that any place in your application where you reference static files, you reference them by the STATIC_URL or MEDIA_URL template variables, like this:

    <img src="{{ STATIC_URL }}images/background.jpg">

For more information, see [Django's _Managing Static Files_](https://docs.djangoproject.com/en/dev/howto/static-files/) documentation.
