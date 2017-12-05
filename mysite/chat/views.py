from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from dwebsocket.decorators import accept_websocket
from django.contrib.auth.models import User
from .models import Chat
from django.db.models import Q
# Create your views here.
clients = {}

off_line = {}
@login_required
def chat(request):
    if request.method == 'GET':
        on_line = []
        for i in clients:
            if (i == request.user.id):
                continue
            user = get_object_or_404(User, id = i)
            on_line.append(user)
        return render(request, 'chat/choose.html', {"on_line": on_line})


def chatwith(request, user_id):
    towhom = get_object_or_404(User, id=user_id)
    history = Chat.objects.filter(Q(from_whom=request.user) | Q(to_whom=request.user)).order_by('created')
    a = "0"
    if int(user_id) in clients:
        a = "1"
    return render(request, 'chat/chat.html', {"towhom": towhom, "history": history, "online": a})

@accept_websocket
def connect(request, user_id):
    if request.is_websocket:
        ## prepare
        key = int(request.user.id)
        to_whom = int(user_id)
        ## add to clients
        add_clients(request, key, to_whom)
        check_off_line_message(key)
        try:
            for message in request.websocket:
                if not message:
                    continue
                message_handler(key,to_whom,message)
        finally:
            delete_clients(request, key, to_whom)

def check_off_line_message(key):
    list = []
    for i in clients[key]:
        for j in clients[key][i]:
            list.append(j)

    if (key in off_line):
        for i in list:
            for j in off_line[key]:
                i.send("<this_is_notification>")
                i.send(str(j))
        off_line.pop(key)


def send_message(sender, list, message):
    for client in list:
        client.send(message)
        if message == "<this_is_notification>":
            client.send(str(sender))

def find_socket(uid1, uid2, message, is_message):
    if (uid2 in clients):
        if (uid1 in clients[uid2]):
            send_message(uid1, clients[uid2][uid1], message)
        elif (is_message):
            all = []
            for i in clients[uid2]:
                for j in clients[uid2][i]:
                    all.append(j)
            send_message(uid1,all, "<this_is_notification>")
    elif (is_message):
        if uid2 not in off_line:
            off_line[uid2] = {}
        off_line[uid2][uid1] = "";




def message_handler(user1, user2, message):
    message = message.decode()
    print (message)
    print (message == "<is_typing>")
    if (message == "<is_typing>"):
        find_socket(user1, user2, message, False)
    else:
        chat = Chat(from_whom=get_object_or_404(User, id = user1),
                    to_whom=get_object_or_404(User, id = user2),
                    content=message)
        chat.save()
        find_socket(user1, user2, message, True)



def add_clients(request, key, to_whom):
    if (key not in clients):
        online_notification(key)
        clients[key] = {}
    if (to_whom not in clients[key]):
        clients[key][to_whom] = []
    clients[key][to_whom].append(request.websocket)

def delete_clients(request, key, to_whom):
    clients[key][to_whom].remove(request.websocket)
    if (len(clients[key][to_whom]) == 0):
        clients[key].pop(to_whom)
    if (not any(clients[key])):
        offline_notification(key)
        clients.pop(key)


def online_notification(key):
    for i in clients:
        if (key in clients[i]):
            for j in clients[i][key]:
                j.send("<nibabashangxianle>")

def offline_notification(key):
    for i in clients:
        if (key in clients[i]):
            for j in clients[i][key]:
                j.send("<nibabaxiaxianle>")