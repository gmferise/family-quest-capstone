from django.http.response import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
)
from django.views.generic import View
from django.middleware.csrf import get_token

from django.shortcuts import HttpResponse, render, redirect
from useraccount.forms import LoginForm
from django.contrib.auth import login, logout, authenticate

class JsonResponseUpdated(JsonResponse):
    status_code = 201

class BaseEndpoint(View):
    """
    | Method         | Use                  |
    | :------------- | :------------------- | 
    | self.ok        | Send 200/json + CSRF |
    | self.done      | Send 201/json + CSRF |
    | self.not_ok    | Send 400             |
    | self.not_found | Send 404             |
    | self.no_perms  | Send 403             |
    """

    def _csrf(self, request, response: HttpResponse):
        response.headers['X-CSRFToken'] = get_token(request)
        return response

    def ok(self, request, data):
        """Sets `X-CSRFToken` header"""
        return self._csrf(request, JsonResponse(data))
    
    def done(self, request, data):
        """Sets `X-CSRFToken` header"""
        return self._csrf(request, JsonResponseUpdated(data))
    
    def not_ok(self):
        return HttpResponseBadRequest()
    
    def not_found(self):
        return HttpResponseNotFound()
    
    def no_perms(self):
        return HttpResponseForbidden()
    
class GenericFormView(View):
    """
    Override NotImplemented methods and functions with appropriate data.
    Handles serving empty forms and validating posted forms.
    _handle_submission() will be called after validation.
    _handle_submission() can return a response like normal to redirect the user
    or serve alternate post-submission content.
    """
    FormClass = NotImplemented
    template_name = "generic_form.html"
    template_text = {"header":"Generic Form", "submit":"Submit"}

    def get(self, request, *args, **kwargs):
        form = self.FormClass()
        return render(request, self.template_name, {"form": form, "template_text": self.template_text})

    def post(self, request, *args, **kwargs):
        form = self.FormClass(request.POST)
        if form.is_valid():
            res = self._handle_submission(request, form.cleaned_data,form)
            if res:
                return res
        return render(request, self.template_name, {"form": form, "template_text": self.template_text})

    def _handle_submission(self, request, form_data,raw_form):
        return NotImplemented

