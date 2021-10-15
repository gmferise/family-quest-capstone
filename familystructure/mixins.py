from urllib.parse import urlparse

from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url

from django.contrib.auth.mixins import LoginRequiredMixin

class PersonRequiredMixin(LoginRequiredMixin):
    login_url = '/signup/about-you/'
    
    """Verify that the current user has a person attached."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.person:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def handle_no_permission(self):

        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )