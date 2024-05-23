from django.urls import path
from .views import (
    home,
    login_user,
    logout_user,
    register,
    question_create,
    question_detail,
    question_update,
    question_delete,
    choices_create,
    question_choice_detail,
    choice_update,
    detail,
    vote,
    results,
)

app_name = "polls"
urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path("questions/create/", question_create, name="question_create"),
    path("questions/<int:question_id>", question_detail, name="question_detail"),
    path("question_update/<int:question_id>", question_update, name="question_update"),
    path("questions/delete/<int:question_id>", question_delete, name="question_delete"),
    path("questions/<int:question_id>/create_choices/", choices_create, name="create_choices"),
    path("questions/<int:question_id>/choices/", question_choice_detail, name="choice_detail"),
    path("questions/choices/<int:choice_id>", choice_update, name="choice_update"),
    path("<int:question_id>/", detail, name="detail"),
    path("<int:pk>/results/", results, name="results"),
    path("<int:question_id>/vote/", vote, name="vote"),
]

