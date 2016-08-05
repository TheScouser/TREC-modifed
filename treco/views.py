# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers
from django.contrib import messages
import json
import urllib
import hmac
import hashlib
import base64

from models import Task, Track, Researcher, Run
from forms import TaskForm, TrackForm, UserForm, ResearcherForm, RunForm, LoginForm, UpdateProfile
from invoker import *


def index(request):
    return render(request, 'treco/index.html', {"profile_picture_url": get_profile_pic(request)})


@staff_member_required
def submit_task(request):
    # Handle file upload
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        print "Checking form..."
        if form.is_valid():
            print "Form is valid..."
            form.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('SubmitRun'))
    else:
        form = TaskForm()  # A empty, unbound form

    # Load documents for the list page
    tasks = Task.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'treco/SubmitTask.html',
        {'tasks': tasks, 'form': form, "profile_picture_url": get_profile_pic(request)},
        context_instance=RequestContext(request)
    )


@staff_member_required
def submit_track(request):
    # Handle file upload
    if request.method == 'POST':
        form = TrackForm(request.POST)
        print "Checking form..."
        if form.is_valid():
            print "Form is valid..."
            form.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('SubmitTask'))
    else:
        form = TrackForm()  # A empty, unbound form
    # Render list page with the documents and the form
    return render_to_response(
        'treco/SubmitTrack.html',
        {'form': form, "profile_picture_url": get_profile_pic(request)},
        context_instance=RequestContext(request)
    )


@login_required
def submit_run(request):
    # Handle file upload
    if request.method == 'POST':
        form = RunForm(request.POST, request.FILES)
        if form.is_valid():  # Validates file contents as well.
            researcher = Researcher.objects.all().get(userid=request.user)
            if researcher:
                run = form.save(commit=False)
                run.researcher = researcher

                ##############################################
                # Get run data from binary file
                print request.FILES.keys()
                path = default_storage.save('tmp/' + run.result_file.name,
                                            ContentFile(request.FILES['result_file'].read()))
                tmp_file_path = os.path.join(settings.MEDIA_ROOT, path)
                print tmp_file_path
                results = getResults(invoke(os.path.normpath(settings.BASE_DIR +
                                                             run.task.judgement_file.url), tmp_file_path))
                print results
                if len(results) == 3:
                    run.map = results["map"]
                    run.p10 = results["P_10"]
                    run.p20 = results["P_20"]
                    print "Form is valid..."
                    run.save()
                    form.save()
                    return redirect('Results/' + run.task.track.track_title + '/' + str(run.task.id) +'/' + str(run.pk))
                else:
                    print "Form invalid or judgement file invalid!"
                default_storage.delete(tmp_file_path)
                #############################################
                # Redirect to the document list after POST

            else:
                print "User not in researcher table."
                return HttpResponseRedirect(reverse('SubmitRun'))
    else:
        form = RunForm()  # A empty, unbound form

    # Render list page with the documents and the form
    return render_to_response(
        'treco/SubmitRun.html',
        {'form': form, "profile_picture_url": get_profile_pic(request)},
        context_instance=RequestContext(request)
    )

def user_login(request):
    if request.method == 'POST':
        usr_login = LoginForm(request.POST)
        if usr_login.is_valid():
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user:
                login(request, user)
                return HttpResponseRedirect('/About.html')
            else:
                return HttpResponse("Invalid login details supplied!")
    else:
        usr_login = LoginForm()
    return render(request, 'treco/Login.html', {"form": usr_login, "profile_picture_url": get_profile_pic(request)})


@login_required
def profile(request):
    context = {"profile_picture_url": get_profile_pic(request)}
    if request.user.is_authenticated():
        researcher = Researcher.objects.get(userid=request.user.id)
        context['researcher'] = researcher
        context['submissions'] = Run.objects.all().filter(researcher=researcher)
    return render_to_response('treco/Profile.html', context, context_instance=RequestContext(request))


def get_profile_pic(request):
    if request.user.is_authenticated():
        researcher = Researcher.objects.get(userid=request.user.id)
        if str(researcher.profile_picture) != "":
            return "/media/" + str(researcher.profile_picture)
    return "/media/profile_pictures/default.png"
        

@login_required
def update_profile(request):
    usr_profile = Researcher.objects.get(userid=request.user.id)
    if request.method == 'POST' and 'info' in request.POST:
        form = UpdateProfile(request.POST, request.FILES, instance=usr_profile)
        # user_form = UserForm(request.POST, instance = request.user)
        if form.is_valid():
            usr_profile = form.save(commit=False)
            usr_profile.save()
            return HttpResponseRedirect('/')
        else:
            print form.errors
    else:
        form = UpdateProfile(instance=usr_profile)
    if request.method == 'POST' and 'changep' in request.POST:
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            print 'Form is valid'
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.is_active = False
            user.save()
            return HttpResponseRedirect('/')
        else:
            print user_form.errors
    else:
        user_form = UserForm(instance=request.user)
    return render(request, 'treco/UpdateProfile.html', {'form': form, 'user_form': user_form, "profile_picture_url": get_profile_pic(request)})


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        researcher_form = ResearcherForm(request.POST, request.FILES)
        if user_form.is_valid():
            if researcher_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.is_active = False
                user.save()
                researcher = researcher_form.save(commit=False)
                researcher.userid = user
                researcher.save()
                registered = True
                return redirect(reverse("Login"))
            else:
                print researcher_form.errors
        else:
            print user_form.errors
    else:
        user_form = UserForm()
        researcher_form = ResearcherForm()

    # Render the template depending on the context.
    return render(request,
                  'treco/Register.html',
                  {'user_form': user_form, 'researcher_form': researcher_form, 'registered': registered, "profile_picture_url": get_profile_pic(request)})


def get_users_runs(request):
    researcher = Researcher.objects.all().filter(userid=request.user.id)[0]
    return Run.objects.all().filter(researcher=researcher)


def get_runs(request, pk):
    if pk == '-1':
        context = serializers.serialize("json", Run.objects.all())
        return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        context = serializers.serialize("json", Run.objects.all().filter(pk=pk))
        return HttpResponse(json.dumps(context), content_type="application/json")


def get_tasks(request):
    context = serializers.serialize("json", Task.objects.all())
    print json.dumps(context)
    return HttpResponse(json.dumps(context), content_type="application/json")


def get_init_data(request):
    context = dict()
    context["tracks"] = serializers.serialize("json", Track.objects.all())
    context["tasks"] = serializers.serialize("json", Task.objects.all())
    context["runs"] = serializers.serialize("json", Run.objects.all())
    display_names = []
    for name in Researcher.objects.all().values("display_name"):
        display_names.append(name)
    context["researchers"] = json.dumps(display_names)
    return HttpResponse(json.dumps(context), content_type="application/json")


def get_runs_for_task(task_pk):
    results = []
    for run in Run.objects.all():
        if run.task.pk == task_pk:
            results.append(run)
    return results


def get_results_for_url(request):
    if request.is_ajax():
        keyword = None
        query_type = None
        run_type = None
        feedback_type = None
        researcher = None
        if request.GET.get('description'):
            keyword = request.GET.get('description')
        if request.GET.get('query_type'):
            query_type = request.GET.get('query_type')
        if request.GET.get('run_type'):
            run_type = request.GET.get('run_type')
        if request.GET.get('feedback_type'):
            feedback_type = request.GET.get('feedback_type')
        if request.GET.get('researcher'):
            researcher = request.GET.get('researcher')
        data = filter(None, request.path.split('/'))[1:]
        results = []
        if len(data) == 0:
            for run in Run.objects.all():
                results.append(run)
        if len(data) == 1:
            for task in Task.objects.all():
                if task.track.pk == data[0]:
                    for run in get_runs_for_task(task.pk):
                        results.append(run)
        elif len(data) == 2:
            for task in Task.objects.all():
                if task.track.pk == data[0]:
                    if task.pk == int(data[1]):
                        for run in get_runs_for_task(task.pk):
                            results.append(run)
        elif len(data) == 3:
            for task in Task.objects.all():
                if task.track.pk == data[0]:
                    if task.pk == int(data[1]):
                        for run in get_runs_for_task(task.pk):
                            if run.pk == int(data[2]):
                                results.append(run)
        if keyword:
            temp_results = []
            for result in results:
                if keyword in result.description:
                    temp_results.append(result)
            results = temp_results
        if query_type:
            temp_results = []
            for result in results:
                if result.query_type == query_type:
                    temp_results.append(result)
            results = temp_results
        if feedback_type:
            temp_results = []
            for result in results:
                if result.feedback_type == feedback_type:
                    temp_results.append(result)
            results = temp_results
        if run_type:
            temp_results = []
            for result in results:
                if result.run_type == run_type:
                    temp_results.append(result)
            results = temp_results
        if researcher:
            temp_results = []
            for result in results:
                if result.researcher.display_name == researcher:
                    temp_results.append(result)
            results = temp_results
        return results
    else:
        raise Http404

        
def visitor(request):
    string = request.path[1:]  # first int
    data = filter(None, string.split('/'))[1:]
    return render(request, 'treco/Visitor.html', {"profile_picture_url": get_profile_pic(request)})        

def result(request):
    string = request.path[1:]  # first int
    data = filter(None, string.split('/'))[1:]
    return render(request, 'treco/Result.html', {"profile_picture_url": get_profile_pic(request)})


def get_results(request):
    results = get_results_for_url(request)
    context = serializers.serialize("json", results)
    return HttpResponse(json.dumps(context), content_type="application/json")


def get_widgets(request):
    widgets = json.load(open("static/specs/widgets.json"))
    return HttpResponse(json.dumps(widgets), content_type="application/json")

def terms(request):
    return render(request, 'treco/terms_and_conditions.html', {"profile_picture_url": get_profile_pic(request)})

def cookie_policy(request):
    return render(request, 'treco/cookie_policy.html', {"profile_picture_url": get_profile_pic(request)})

@login_required
def about(request):
    url = "https://www.periscopedata.com/api/embedded_dashboard?data={data}&signature={signature}"
    data = {
        "dashboard": 61406,
        "embed": "true",
        "daterange": {"days": 7},
        "aggregation": "daily",
        "visible": ["aggregation","daterange"]
    }
    encoded_data = urllib.quote_plus(json.dumps(data))
    print (encoded_data)
    message =('/api/embedded_dashboard?data=' + encoded_data).encode('utf-8')
    secret = "9ae8afe1-a047-463e-a015-f0b90d92".encode('utf-8')
    signature = hmac.new(secret, message, digestmod=hashlib.sha256).hexdigest()
    print(signature)
    url = url.format(data=encoded_data,signature=signature)
    return render(request, 'treco/About.html', {"profile_picture_url": get_profile_pic(request),"dashboard_url": url})