from django.contrib.auth import authenticate, login, logout
from django.db import Error
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from app.models import User, Instruction, Test, TestToUser


# Create your views here.

class HomePageView(View):

    def get(self, request):
        if request.user.is_authenticated:
            instructions = Instruction.objects.all()
            if request.GET.get('search'):
                instructions = instructions.filter(
                    Q(title__contains=request.GET.get('search'))|
                    Q(short_description__contains=request.GET.get('search')),
                )
            return render(request, 'index.html', context={
                "instructions": instructions
            })
        return redirect("authorization")


class PersonalAreaPageView(View):

    def get(self, request):
        tests_to_user = TestToUser.objects.filter(user=request.user)
        if request.GET.get('search'):
            tests_to_user = tests_to_user.filter(
                Q(test__title__contains=request.GET.get('search'))
            )
        return render(request, 'personal_area.html', context={
            'tests': tests_to_user
        })


class TestsPageView(View):

    def get(self, request):
        tests = Test.objects.all()
        if request.GET.get('search'):
            tests = tests.filter(
                Q(title__contains=request.GET.get('search'))
            )
        return render(request, 'tests.html', context={
            'tests': tests
        })


class AuthorizationPageView(View):

    def get(self, request):
        return render(request, 'authorization.html')

    def post(self, request):
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect("home")
        return render(request, 'authorization.html', context={
            "error": "Ошибка авторизации, попробуйте снова"
        })


class RegistrationPageView(View):

    def get(self, request):
        return render(request, 'registration.html')

    def post(self, request):
        try:
            User.objects.create_user(
                username=request.POST.get("username"),
                email=request.POST.get("email"),
                password=request.POST.get("password")
            )
        except Error:
            return render(request, 'registration.html', context={
                "error": "Ошибка регистрации, попробуйте снова"
            })
        else:
            return redirect("authorization")


def user_logout(request):
    logout(request)
    return redirect("home")


class InstructionDetailView(View):

    def get(self, request, id):
        instruction = Instruction.objects.get(id=id)
        tests = Test.objects.filter(instruction=instruction)
        return render(request, 'instruction.html', context={
            'instruction': instruction,
            'tests': tests
        })


class TestDetailView(View):

    def get(self, request, id):
        test = Test.objects.get(id=id)
        return render(request, 'test.html', context={
            'test': test,
        })


class GetScoreForeTestView(View):

    def post(self, request, id):
        test = Test.objects.get(id=id)
        count_true_answer = 0
        for key, value in request.POST.dict().items():
            if key.split("_")[0] == "answer" and request.POST.get(key) == "True":
                count_true_answer += 1
        count_total_answer = test.question_set.all().count()
        result = (count_true_answer / count_total_answer) * 100

        test_to_user = TestToUser.objects.filter(user=request.user, test=test)
        if not test_to_user.exists():
            if result < 50:
                TestToUser.objects.create(test=test, user=request.user, score=2)
            elif 50 <= result <= 60:
                TestToUser.objects.create(test=test, user=request.user, score=3)
            elif 60 < result <= 80:
                TestToUser.objects.create(test=test, user=request.user, score=4)
            else:
                TestToUser.objects.create(test=test, user=request.user, score=5)
        else:
            test_to_user = test_to_user.first()
            if result < 50:
                test_to_user.score = 2
            elif 50 <= result <= 60:
                test_to_user.score = 3
            elif 60 < result <= 80:
                test_to_user.score = 4
            else:
                test_to_user.score = 5
            test_to_user.save()
        return redirect("personal_area")
