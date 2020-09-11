from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import hashlib
import time

from redis import from_url

from .forms import GetCode


def get_name(request):
    r = from_url("redis://redis:6379")
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GetCode(request.POST)
        # check whether it's valid:
        if form.is_valid():
            code = form.cleaned_data['code']
            stdin = form.cleaned_data['stdin']
            lang = form.cleaned_data['language']
            token = hashlib.sha256(code.encode()).hexdigest()
            r.lpush("tasks", f"{token}\n{lang}\n{stdin}{token}{code}")
            url = f'/token/{token}/'
            time.sleep(1)
            return HttpResponseRedirect(url)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GetCode()

    return render(request, 'code_submit.html', {'form': form})


def get_code_result(request, token):
    r = from_url("redis://redis:6379")
    res = r.get(token)
    if res:
        return render(request, 'code_result.html', {'result': res.decode()})
    else:
        return render(request, 'wait_for_code.html')
