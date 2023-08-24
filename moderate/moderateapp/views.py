from django.shortcuts import render
from .models import Module, Issue

def home(response):
    return render(response, "moderate/home.html", {})


def find(response):
    return render(response, "moderate/find.html")

def moderate(request):
    mydict = {}
    text = request.POST.get('mod')
    text = text.upper()
    mydict["text"] = text
    try:
        # check if mod is in database
        comments = Module.objects.get(code=text)
        mydict["rating"] = getattr(comments, "rating")

        mydict["comment1"] = getattr(comments, "comment1")
        if mydict["comment1"] == "NULL":
            mydict["comment1"] = ''

        mydict["comment2"] = getattr(comments, "comment2")
        if mydict["comment2"] == "NULL":
            mydict["comment2"] = ''

        mydict["comment3"] = getattr(comments, "comment3")
        if mydict["comment3"] == "NULL":
            mydict["comment3"] = ''
            
        mydict["emotions"] = list(map(float, getattr(comments, "emotions").split(",")))
        Module.objects.filter(code=text).update(searched=
                                                getattr(comments, "searched") + 1)
        
    except Exception as e:
        # if not return error page
        print(e)
        return render(request, "moderate/error.html", {})

    global cmod
    cmod = text
    return render(request, "moderate/comments.html", mydict)

def view(response):
    return render(response, "moderate/view.html")

def rating(response):
    mydict = {}
    top3 = Module.objects.order_by("-rating")[:3]
    mydict["first"] = getattr(top3[0], "code")
    mydict["second"] = getattr(top3[1], "code")
    mydict["third"] = getattr(top3[2], "code")
    mydict["rate1"] = getattr(top3[0], "rating")
    mydict["rate2"] = getattr(top3[1], "rating")
    mydict["rate3"] = getattr(top3[2], "rating")
    return render(response, "moderate/rating.html", mydict)

def searched(response):
    mydict = {}
    top3 = Module.objects.order_by("-searched")[:3]
    mydict["first"] = getattr(top3[0], "code")
    mydict["second"] = getattr(top3[1], "code")
    mydict["third"] = getattr(top3[2], "code")
    mydict["search1"] = getattr(top3[0], "searched")
    mydict["search2"] = getattr(top3[1], "searched")
    mydict["search3"] = getattr(top3[2], "searched")
    return render(response, "moderate/searched.html", mydict)

def problem(request):
    return render(request, "moderate/problem.html")

def thankyou(request):
    text = request.POST.get('problem')
    issue = Issue(code=cmod,message=text)
    issue.save()
    return render(request, "moderate/thankyou.html")
    