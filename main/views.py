from django.shortcuts import render, redirect
from .models import Tutorials, TutorialCategory, TutorialSeries
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views
def single_slug(request, single_slug):
    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    if single_slug in categories:
        matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)
        series_urls = {}
        for m in matching_series.all():
            part_one = Tutorials.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest("tutorial_created")
            series_urls[m] = part_one.tutorial_slug
        return render(request, 'main/category.html', context= {"part_ones": series_urls})

    tutorials = [t.tutorial_slug for t in Tutorials.objects.all()]
    if single_slug in tutorials:
        this_tutorial = Tutorials.objects.get(tutorial_slug=single_slug)
        tutorials_from_series = Tutorials.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by("tutorial_created")

        this_tutorial_idx = list(tutorials_from_series).index(this_tutorial)

        return render(request, 'main/tutorial.html', context={'tutorial': this_tutorial,
                                                              "side_bar": tutorials_from_series,
                                                              "this_tutorial_idx": this_tutorial_idx})

    return HttpResponse(f"{single_slug} does not correspond to anything")


def home(request):
    context = {"categories": TutorialCategory.objects.all}
    return render(request, 'main/categories.html', context)


def register(request):
    form = CreateUserForm

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'account was created for ' + user)
            return redirect('login')
    context = {"form": form}
    return render(request, 'main/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('your_name')
        password = request.POST.get('your_pass')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homeview')
        else:
            messages.info(request, 'username or password is incorrect')
            return redirect('login')
    context = {}
    return render(request, 'main/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
