from django.http import Http404, HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice
from django.db.models import F, Q
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import QuestionForm, ChoicesForm

def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("polls:home"))


    if request.method == 'POST':
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("polls:home"))
        else:
            messages.error(request, ('Username or password does not exist'))
   
    context = {}
    return render(request, 'polls/login.html', context)

def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('polls:home'))

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data = request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username, 
                password=request.POST['password1'])
            login(request, authenticated_user)

    return render(request, 'polls/register.html', {'form': form})


def home(request):
    questions = Question.objects.all().order_by("-pub_date")
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        print(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(request, "Successfully Created A Question")
            return HttpResponseRedirect(reverse('polls:home'))
        else:
            messages.error(request, "Not Successfully Created")
    context = {"questions": questions, "form": form}
    return render(request, "polls/home.html", context)

def question_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # if not request.user.is_authenticated():
    #     raise Http404
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        print(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(request, "Successfully Created A Question")
            return HttpResponseRedirect(reverse('polls:question_detail', args=[instance.id]))
        else:
            messages.error(request, "Not Successfully Created")
    context = {
        "form": form, 
    }
    return render(request, "polls/question_form.html", context)

def question_detail(request, question_id):
    instance = get_object_or_404(Question, pk=question_id)
    # if not request.user.is_staff or not request.user.is_superuser:
    #         raise Http404
    context = {
        "question_id": question_id,
        "question_text": instance.question_text,
    }
    return render(request, "polls/question_detail.html", context)

def question_update(request, question_id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Question, pk=question_id)
    form = QuestionForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, "Question Updated")
        return HttpResponseRedirect(reverse('polls:question_detail', args=[instance.id]))
    context = {
        "instance": instance,
        "form": form,
    }
    return render(request, "polls/question_update.html", context)

def question_delete(request, question_id):
    question = Question.objects.get(pk=question_id)
    question.delete()
    messages.success(request, ('This Question Had Been Deleted'))
    return HttpResponseRedirect(reverse('polls:home'))

def choices_create(request, question_id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    question = get_object_or_404(Question, pk=question_id)

    form_choices = ChoicesForm()
    if request.method == 'POST':
            form_choices = ChoicesForm(request.POST)
            print(request.POST)
            if form_choices.is_valid():
                instance = form_choices.save(commit=False)
                instance.question = question
                instance.save()
                return HttpResponseRedirect(reverse('polls:question_detail', args=[question.id]))
    context = {'form_choices': form_choices}
    return render(request, "polls/choices_form.html", context)

def question_choice_detail(request, question_id):
    qs = Question.objects.prefetch_related("choice_set").get(pk=question_id)
    choices = qs.choice_set.all()
    print(question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {
        "choices": choices,
        "question": question,
    }
    return render(request, "polls/choice_detail.html", context)

def choice_update(request, choice_id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    choice = get_object_or_404(Choice, pk=choice_id)
    choice_obj = Choice.objects.select_related("question").get(pk=choice_id)
    question_id = choice_obj.question.id
    form = ChoicesForm(request.POST or None, instance=choice)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, "Choice Updated")
        return HttpResponseRedirect(reverse('polls:choice_detail', args=[question_id]))
    context = {
        "choice": choice,
        "form": form,
    }
    return render(request, "polls/question_update.html", context)





def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        print(request.POST)
        print(selected_choice)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.voter = request.user
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
       

def results(request, pk):
    question = get_object_or_404(Question, pk=pk)
    context = {
        "question": question,
    }
    return render(request, "polls/results.html", context)