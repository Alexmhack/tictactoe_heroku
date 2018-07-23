from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Game
from .forms import MoveForm


@login_required
def game_detail(request, id):
	game = get_object_or_404(Game, pk=id)
	context = {'game': game}
	# checking if this is user's move, then passing a form in dict for MoveForm fields
	if game.is_users_move(request.user):
		context['form'] = MoveForm()
	return render(request, 'gameplay/detail.html', context)


# function for making moves 
@login_required
def make_move(request, id):
	# make a game instance
	game = get_object_or_404(Game, pk=id)
	
	# if this is not user's turn we don't raise error
	if not game.is_users_move(request.user):
		raise PermissionDenied

	# we make a new move from the Game method
	move = game.new_move()

	# we make a form with the user's data
	form = MoveForm(instance=move, data=request.POST)
	if form.is_valid():
		move.save()
		return redirect('gameplay_detail', id)
	# if wrong we show the form again
	else:
		return render(request, 'gameplay/detail.html', {
				'game': game,
				'form': form
			})
