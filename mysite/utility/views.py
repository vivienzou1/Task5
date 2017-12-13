from django.shortcuts import render
from account.forms import *
# Create your views here.
def is_enough(owner, amount):
    if owner.balance < amount:
        #print (owner.balance)
        #print (amount)
        #print (owner.balance < amount)
        return False
    else:
        return True

def is_frozen(profile):
    return profile.account.account_status == 'frozen'