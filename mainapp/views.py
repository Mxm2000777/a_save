import sys, json, os
from random import randint
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
import datetime
sys.path.append('a_save/')
from re_selfdb import SQLITE
db = SQLITE('db_asave.sqlite3')
def deor(x):
    y = x.replace("'", '"')
    return json.loads(y)
def checkadm(request):
    pass
def setid(v, username=None):
    x = randint(2, 99999999)
    if v == "user":
        for i in db.getcolumns("id"):
            if db.get(i, "username") == username:
                return i
        if x in db.getcolumns("id"):  # ЧТОБЫ НЕ РЕШГАЛИСЬ ЕСЛИ ЛОГИН УЖЕ ЕСТЬ
            return setid(v, username)
        return str(x)
    if v == "news":
        for i in db.getcolumns("news"):
            if x in deor(i).keys():
                return setid(v, username)
def getava(idd):
    if not os.path.isfile(f"C:/Users/mxm20/a_save/mainapp/media/{idd}.png"):
        y = "/static/images/nop.png" 
    else: 
        y = f"/media/{idd}.png"
    return y
def pere(request, url, context, theme=None):
    if context is None:
        context = {}
    context["request"] = request
    if theme is None:
        theme = "white"
    idd = request.COOKIES.get("idd")
    if idd is None:
        if url is None:
            url = 'base.html'
        else:
            context['lnk'] = 'base.html'
        context["idd"] = idd
    if not idd is None:
        if url is None:
            url = 'logged.html'
        else:
            context['lnk'] = 'logged.html'
        context["idd"] = idd
    return render(request, f'{url}', context)
def index(request):
    return pere(request, None, None)
def reg_page(request):
    if request.method == "GET":
        return render(request, "reg.html")
    if request.method == 'POST':
        username, password1, password2 = request.POST.get("username"), request.POST.get("pswd1"), request.POST.get("pswd2")
        idd = setid("user", username)
        if password1 != password2:
            return HttpResponse("<h3>Пароли должны совпадать</h3>")
        else:
            db.set(idd, 'passwords', password1)
            db.set(idd, "username", username)
            db.set(idd, "news", "{}")
            r = render(request, "logged.html", {'name' : 'Вы успешно зарегались', "user_name": username})
            r = HttpResponseRedirect("base")
            r.set_cookie("idd", idd)
            return r
def login_page(request):
    if request.method == "GET":
        return render(request, "login_page.html", {"idd": request.COOKIES.get("idd"), "error": "Добро пожаловать в Asave"})
    if request.method == 'POST':
        username = request.POST.get("username")
        if not username in db.getcolumns("username"):
            return render(request, "login_page.html", {'error': 'Пользователь c таким логином не найден'})
        for i in db.getcolumns("id"):
            if db.get(i, "username") == username:
                if db.get(i, "passwords") == request.POST.get("pswd1"):
                    context = {'error' : 'Вы успешно вошли в аккаунт', 'lnk': 'logged.html'}
                    r = HttpResponseRedirect('base')
                    r.set_cookie("idd", i)
                    return r
                else:
                    context = {'error' : 'Неверный пароль'}
                    return render(request, 'login_page.html', context)
def logout_page(request):
    response = HttpResponseRedirect('base')
    response.delete_cookie('idd')
    return response
def changeprofile(request):
    if request.method == "GET":
        if request.COOKIES.get('idd') is None:
            return pere(request, "login_page.html", {"error": "Войдите в аккаунт", "ok": "/static/images/nop.png"})
        else:
            return pere(request, "changeprofile.html", None)
    if request.method == "POST":
        idd = request.COOKIES.get("idd")
        newnick = request.POST.get("new_username")
        password = request.POST.get('new_pswd')
        myfile = request.FILES.get("new_ava") #берем файл из POST запроса
        path = "C:/Users/mxm20/a_save/mainapp/media"
        if request.POST.get("old_pswd") == "":
            pass
        elif not db.get(idd, "passwords") == request.POST.get("old_pswd"):
            return pere(request, "profile.html", {"error": "Неправильный пароль"})
        if password != "":
            db.set(idd, "passwords", password)
        print(myfile)
        if not newnick == "":
            db.set(idd, "username", newnick)
        if not myfile == None:
            fs = FileSystemStorage(location='mainapp/media/') 
            x = f"{idd}.png" #имя файла
            print(x)
            filename = fs.save(x, myfile) #сохраняем файл из POSt запроса в папку folder
            os.replace(f"{path}/{filename}", f"{path}/{idd}.png")
        return HttpResponseRedirect(f'profile/{idd}')
def profile(request, idd):
    print("профиль:", idd)
    if request.method == "GET":
        y = f"/media/{idd}.png"
        if not os.path.isfile(f"C:/Users/mxm20/a_save/mainapp/media/{idd}.png"):
            y = "/static/images/nop.png" 
        row = db.getall(idd)
        if idd == "None":
            row = None
            su = 0
            context = {"error": idd, "ok": y, "row": row, "user_name": None, "coc": su}
        else:
            if not db.get(idd, "completedorders") == None:
                su = len(list(deor(db.get(idd, "completedorders")).keys()))
            else:
                su = 0
            context = {"error": idd, "ok": y, "row": row, "user_name": row[2], "coc": su}
        if idd == request.COOKIES.get("idd"):
            return pere(request, "myprofile.html", context)
        return pere(request, 'profile.html', context)
def create_news(request):
    if request.method == "GET":
        return pere(request, "create_news.html", None)
    if request.method == "POST":
        idd = request.COOKIES.get("idd")
        x = [db.get(idd, "username"), request.POST.get("headd"), request.POST.get("desk"), datetime.datetime.now().isoformat().replace(":", "_"), 0]
        news = deor(db.get(idd, "news"))
        news[setid("news")] = x
        db.set(idd, "news", str(news))
        return pere(request, "logged.html", None)
def orders(request, idd=None, r=None, idorder=None, n=None):
    context = {"lst": [], "oo": {}, "tags": {}}
    for i in db.all():
        x = deor(i[n])
        if x == []:
            continue
        if r == "render":
            context["lst"].append(x)
            context["rating"] = i[5]
            context["username"] = i[12]
        if r =="rr":
            if i[11] == "[]":
                continue
            print(str(list(i)))
            context["lst"].append(i) #x = [1, 2, 2]  #{ok: x}
            context["oo"][i[0]] = deor(i[11].replace("'", '"'))
            context["tags"][i[0]] = deor(i[11].replace("'", '"'))[1].split(",")
        if r == "delete":
            for j in list(x.keys()):
                if j == idorder:
                    del x[idorder]
                    return pere(request, 'orders.html', context)
        if r == "find":
            for k in x.keys():
                iddd = x[k][0]
                if k == idorder and iddd == idd:
                    user_name = db.get(iddd, "username")
                    return pere(request, "myorder.html", {"idorder": idorder, "username": user_name})
                if k == idorder:
                    return pere(request, "order.html", {"idorder": idorder, "ootk": "false", "otk": "Откликнутся"})
        print(i[0])
    if r == "rr":
        return pere(request, "specialists.html", context)
    return pere(request, 'orders.html', context)