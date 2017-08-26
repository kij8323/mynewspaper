from django.shortcuts import render

# Create your views here.
from .models import Scorebill
from accounts.models import MyUser
# Create your views here.
def scorebillpage(request, user_id):
	user = MyUser.objects.get(id = user_id)
	scorebill = Scorebill.objects.filter(user = user).order_by('-id')
	context = {
		'scorebill': scorebill,
	}
	return render(request, 'scorebillpage.html',  context)

def scorerankpage(request):
	scorerank = MyUser.objects.exclude(pk=53).exclude(pk=519).order_by('-score')[0:10]

	context = {
		'scorerank': scorerank,
	}
	return render(request, 'scorerankpage.html',  context)
