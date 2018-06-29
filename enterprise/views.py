# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from enterprise.models import *
from menu.models import *
from cart.views import *
from order.models import *


def main_view(request):

    # sEnterprise = request.session.get('enterprise', 'enterprise')
    # sTable = request.session.get('table', 'table')
    # enterprise = get_object_or_404(Enterprise, name=sEnterprise)

    context = {}
    # context = {'enterprise': enterprise, 'table': sTable, 'enterprise': enterprise}
    return render(request, "enterprise/index.html", context)



def login_view(request):

    # sEnterprise = request.session.get('enterprise', 'enterprise')
    # sTable = request.session.get('table', 'table')
    # enterprise = get_object_or_404(Enterprise, name=sEnterprise)

    # add_line_view(request)

    # cartSession = request.session['cart']

    context = {}
    # context = {'enterprise': enterprise, 'table': sTable, 'enterprise': enterprise}
    return render(request, "registration/login.html", context)








