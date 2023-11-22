import sys, json, os
from random import randint
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
import datetime
from django.views import View
sys.path.append('a_save/')
from re_selfdb import SQLITE
db = SQLITE('db_asave.sqlite3')
db1 = SQLITE("chats.sqlite3")
def setid(v, username=None):
    x = randint(2, 99999999)
    if v == "user":
        for i in db.getcolumns("id"):
            if db.get(i, "username") == username:
                return i
        if x in db.getcolumns("id"):  # ЧТОБЫ НЕ РЕШГАЛИСЬ ЕСЛИ ЛОГИН УЖЕ ЕСТЬ
            return setid("chat", username)
        return str(x)
    if v == "chat":
        if x in db1.getcolumns("id"):
            return setid("chat")
        return str(x)

def getava(idd):
    if not os.path.isfile(f"C:/Users/dos12/.vscode/re_self/mainapp/media/{idd}.png"):
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
    #if not user__name or user__name == None:
    idd = request.COOKIES.get("idd")
    if idd is None:
        context['lnk'] = 'a_save/base.html'
        context["idd"] = idd
    if not idd is None:
        context['lnk'] = 'a_save/logged.html'
        context["idd"] = idd
    #else:
       #
    return render(request, f'a_save/{url}', context)
def index(request):
    print("index")
    idd = request.COOKIES.get('idd')
    
    if idd != None:
        username = db.get(idd, "username")
        return render(request, "a_save/logged.html", {"user_name": username, "idd": idd})
    else:
        return render(request, 'a_save/base.html', {"user_name": None, "idd": idd})

def reg_page(request):
    if request.method == "GET":
        return render(request, "a_save/test1.html")
    if request.method == 'POST':
        data = request.POST
        username = data.get("username")
        idd = setid("user", username) #+ datetime.datetime.now().isoformat()[:19]
        email = data.get("email")
        phone = data.get('phone')
        password1, password2 = data.get("pswd1"), data.get("pswd2")
        if password1 != password2:
            return HttpResponse("<h3>Пароли должны совпадать</h3>")
        else:
            db.set(idd, 'passwords', password1)
            db.set(idd, "email", email)
            db.set(idd, "phone", phone)
            db.set(idd, "desc", 0)
            db.set(idd, "city", data.get("city"))
            db.set(idd, "createdorders", "{}")
            db.set(idd, "completedorders", "{}")
            db.set(idd, "rating", "Нету")
            db.set(idd, "chats", "{}")
            db.set(idd, "orders", "{}")
            db.set(idd, "portfolio", "[]")
            db.set(idd, "username", username)
            context = {'name' : 'Вы успешно зарегались', "user_name": username}
            r = render(request, "a_save/logged.html", context)
            r = HttpResponseRedirect("base")
            r.set_cookie("idd", idd)
            return r
def login_page(request):
    if request.method == "GET":
        return render(request, "a_save/login_page.html", {"idd": request.COOKIES.get("idd")})
    if request.method == 'POST':
        data = request.POST
        username = data["username"]
        if not username in db.getcolumns("username"):
            context = {'error': 'Пользователь c таким логином не найден'}
            return render(request, "a_save/login_page.html", context)
        for i in db.getcolumns("id"):
            if db.get(i, "username") == username:
                if db.get(i, "passwords") == data["pswd1"]:
                    context = {'error' : 'Вы успешно вошли в аккаунт', 'lnk': 'a_save/logged.html'}
                    r = HttpResponseRedirect(f'profile/{i}')
                    r.set_cookie("idd", i)
                    return r
                else:
                    context = {'error' : 'Неверный пароль'}
                    return render(request, 'a_savef/login_page.html', context)
        
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
            ok = f"/media/{filename[:len(idd)]}.png"
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
            context = {"error": idd, "ok": y, "row": row, "user_name": row[12], "coc": su}
        if idd == request.COOKIES.get("idd"):
            return pere(request, "myprofile.html", context)
        return pere(request, 'profile.html', context)
    if request.method == "POST":
        y = request.POST.get("ok")
        #x = broadcast(y)
        #x1 = send(None, y)
        #print(x, x1)
        return HttpResponseRedirect(f"/ws/{idd}")
        return pere(request, "profile.html", None)
def create_order(request):
    # 
    # blank = [b1, b2, b3]
    # b1 = [заголовок, описание, цена, tags, отклики, time, ] 
    # tags = [t1, t2, t3]
    if request.method == 'GET':
        return render(request, "a_save/create_order.html")
    else:
        data = request.POST
        zag = data["zag"]
        desc = data["desc"]
        price = data["price"]
        myfile = request.FILES.get("orderpic")
        print(myfile, request.FILES)
        tags = data["tags"].replace(" ", "").split(",")
        otk = []
        time = datetime.datetime.now().isoformat()
        idd = request.COOKIES.get("idd")
        idorder = f"{idd}_{time}"
        
        x = json.loads(db.get(idd, "createdorders").replace("'", '"'))
        if not myfile == None:
             
            fs = FileSystemStorage(location='mainapp/media/') 
            pic = f"{idorder}.png".replace(":", "_") #имя файла
            filename = fs.save(pic, myfile) #сохраняем файл из POSt запроса в папку folder
            ok = f"/media/{filename[:len(idorder)]}.png"
        else:
            ok = "/static/images/nop.png" 
        x[idorder.replace(":", "_")] = [idd, zag, desc, price, tags, otk, time, ok, db.get(idd, "username")]
        db.set(idd, "createdorders", str(x))
        context = {'name' : 'Заказ создан'}
        return render(request, 'a_save/logged.html', context)
def create_blank(request):
    if request.method == "GET":
        return pere(request, "create_blank.html", None)
    if request.method == "POST":
        idd = request.COOKIES.get("idd")
        x = [request.POST.get("price"), request.POST.get("tags"), "[]", db.get(idd, "username")]
        db.set(idd, "portfolio", str(x))
        db.set(idd, "desc", request.POST.get("desc"))
        return pere(request, "logged.html", None)
def deor(x):
    y = x.replace("'", '"')
    return json.loads(y)
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
        if r == "otk":
            for k in list(x.keys()):
                
                if k == idorder:
                    return x
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
def renderorders(request):
    x = orders(request, None, "render", None, 8)
    return x
def deleteorder(request, idorder):
    return orders(request, None, "delete", idorder, 8)
def otk(request, idorder):
    idd = request.COOKIES.get("idd")
    x = orders(request, idd, "otk", idorder, 8)
    x[idorder][5].append(idd)
    db.set(idd, "orders", str(x[idorder]))
    return pere(request, "order.html", {"otk" : "Вы_откликнулись", "ootk": "true"})
def completeorder(request):
    pass
def order(request, idorder):
    idd = request.COOKIES.get("idd")
    if request.method == "GET":
        print(idorder)
        return orders(request, idd, "find", idorder, 8)     
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("true") == "true":
            return pere(request, "order.html", None)
        print(request.method)
def clicker(request):
    return pere(request, 'clicker1.html', None)
def specialists(request):
    return orders(request, None, "rr", None, 11)
def ls(request, peopleidd):
    idd = request.COOKIES.get("idd")
    
    if request.method == "GET":
        time = datetime.datetime.now().isoformat().replace(":", "_")
        if not db1.has(idd+time):
            x = sorted([idd, peopleidd])
            chat_id = f"{x[0]}_{x[1]}"
            chat_info = {"ls": True, "admin": sorted([idd, peopleidd]), "created_at": time, "avatar" : {idd : getava(peopleidd), peopleidd : getava(idd)}}
            db1.set(chat_id, "chats_info", str(chat_info))
            db1.set(chat_id, "messages", "{}")
            db1.set(chat_id, "users", str(sorted([idd, peopleidd])))
            return render(request, "re_self/chat.html")
        return render(request, "re_self/chat.html", {"chat": deor(db.get(chat_id, "messages"))})
    if request.method == "POST":
        msg = request.POST.get("msg")
        dt = datetime.datetime.now().isoformat().replace(":", "_")
        x = [msg, idd, 0, request.body.decode('utf-8')]
        ok = sorted([idd, peopleidd])
        chat_id = f"{ok[0]}_{ok[1]}"
        msgs = deor(db1.get(chat_id, "messages"))
        msgs[dt] = x
        db1.set(chat_id, "messages", str(msgs))
        xx = deor(db1.get(chat_id, "messages"))
        print(xx)
        xxx = sorted(list(xx.keys()))
        print(request.body.decode('utf-8'))
        xxxx = db.get(chat_id, "messages")
        return render(request, "re_self/chat.html", {"chat": xx})
def create_group(request, chat_id):
    if request.method == "GET":
        username = request.COOKIES.get("username")
        chat_info = {"admin": [chat_id, username], }
        db1.set(request.COOKIES.get("username"), "chats_info", str(chat_info))
        return render(request, "re_self/chat.html", {"chat_box_name": chat_id})
    if request.method == "POST":
        pass
def chat_box(request, chat_id):
    # we will get the chatbox name from the url
    if request.method == "GET":
        username = request.COOKIES.get("username")
        chat_info = {"admin": [chat_id, username], }
        db1.set(request.COOKIES.get("username"), "chats_info", str(chat_info))
        return render(request, "re_self/chat.html", {"chat_box_name": chat_id})
    if request.method == "POST":
        print(request.POST.get("msg"))
        username = request.COOKIES.get("username")
        msg = username + "$" + request.POST.get("msg")
        chats = deor(db.get(str(sorted(username, chat_id)), "id"))
        if not chat_id in chats.keys():
            ind = 0
            chats[chat_id] = []
        else:
            ind = chats[chat_id][-1][0] + 1
        chats[chat_id].append([ind, msg, datetime.datetime.now().isoformat().replace(":", "-"), username])
        print(chats)

        return pere(request, "chat.html", {"chat_box_name": chat_id, "chat": chats[chat_id]})