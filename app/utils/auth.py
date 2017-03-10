from django.http import Http404

def auth_check(fn):
    def wrapper(*args, **kwargs):
        request = args[0]
        # if we not superuser status or suff status we won't be get it
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
        if not request.user.is_authenticated():
            raise Http404

        return fn(*args, **kwargs)

    return wrapper