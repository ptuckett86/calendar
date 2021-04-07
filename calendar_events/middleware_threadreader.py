try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

from django.utils.deprecation import MiddlewareMixin


def get_current_user():
    return getattr(_thread_locals, "user", None)


class ThreadLocals(MiddlewareMixin):
    def process_request(self, request):
        _thread_locals.user = getattr(request, "user", None)
