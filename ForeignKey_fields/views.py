from django.shortcuts import render
from .forms import BookForm


def creaye(request):
	if form.method == 'POST:
		if form.is_valid():
			cd = form.cleaned_data
			Book.objects.create(category=cd['category'], name=cd['name'], image=cd['image'])
	else:
		from = BookForm(request.user)
	
	return render(request, ...., {'form':form})
