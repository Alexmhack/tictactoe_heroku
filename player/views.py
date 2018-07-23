from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from gameplay.models import Game
from .models import Invitation
from .forms import InvitationForm

@login_required
def home(request):

	# request.user checks if logged in
	# but is bad practise to use too much models code.
	# check the gameplay models for the other code.

	"""
	game_first_player = Game.objects.filter(
		first_player=request.user,
		status='F',
	)
	game_second_player = Game.objects.filter(
		second_player=request.user,
		status='S',
	)

# explicitly coverting queryset into list and adding them.
	context = list(game_first_player) + \
				list(game_second_player)
	"""

	my_games = Game.objects.games_for_user(request.user)
	active_games = my_games.active()
	invitations = request.user.invitations_received.all()

	context = {
		'games': active_games,
		'invitations': invitations,
	}
	
	return render(request, "player/home.html", context)


@login_required
def new_invitation(request):
	# if the method is POST
	if request.method == "POST":
		# creating a instance of the Invitation class that has
		# only from_user which is the current user.
		invitation = Invitation(from_user=request.user)
		# 'data' holds the actual data that the form holds
		form = InvitationForm(instance=invitation, data=request.POST)
		# instance saves the user details and fills all the required
		# details

		# returns True only if all the fields are correctly entered
		# don't forget to use the {% csrf_token %} inside the forms
		# always validate the forms like below in forms
		if form.is_valid():
			form.save()
			# if true then saves to database and returns to home
			return redirect("player_home")
	# else if the method is GET then render the form page again
	else:
		form = InvitationForm()
	return render(request, "player/new_invitation_form.html", {'form': form})


@login_required
def accept_invitation(request, id):
	invitation = get_object_or_404(Invitation, pk=id)
	if not request.user == invitation.to_user:
		raise PermissionDenied
	if request.method == 'POST':
		if 'accept' in request.POST:
			game = Game.objects.create(
				first_player=invitation.to_user,
				second_player=invitation.from_user,
			)
		invitation.delete()

		# redirect takes in the url but we pass the Game instance because this class has get_absolute_url so calling this with redirect will redirect me to the page with this game.
		return redirect(game)
	else:
		return render(request, 
			"player/accept_invitation_form.html",
			{'invitation': invitation})

