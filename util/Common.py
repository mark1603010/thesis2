from django.shortcuts import render, HttpResponse,HttpResponseRedirect,get_object_or_404
from django.urls import reverse,reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum,F,FloatField,Q
from django.views import View
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from util.Util import *
from django.core.signing import Signer
signer = Signer()