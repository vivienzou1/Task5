import threading
from django.conf.urls import *
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from dwebsocket.decorators import accept_websocket


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

def base_view(request):
    #return render(request,'index.html', )

    return render(request, "index.html", {})


clients = []

@accept_websocket
def echo(request):
    if request.is_websocket:
        #lock = threading.RLock()
            #lock.acquire()
        clients.append(request.websocket)
        for mes in request.websocket:
            print (request.websocket)

            a = clients[0].read()
            print (a)

            #lock.release()

urlpatterns = [
    # Example:
    url(r'^$', base_view),
    url(r'^echo$', echo),]


