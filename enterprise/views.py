# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from enterprise.models import *
from menu.models import *
from cart.views import *
from order.models import *


@login_required
def main_view(request):

    # sEnterprise = request.session.get('enterprise', 'enterprise')
    # sTable = request.session.get('table', 'table')
    # enterprise = get_object_or_404(Enterprise, name=sEnterprise)

    context = {}
    # context = {'enterprise': enterprise, 'table': sTable, 'enterprise': enterprise}
    return render(request, "enterprise/index.html", context)





def logout_view(request):
    if request.user:
        logout(request) 
    return redirect('enterprise:login')







