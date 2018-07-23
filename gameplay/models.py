from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


# these are game values with corresponding letter.
GAME_STATUS_CHOICES = (
	('F', 'First Player To Move'),
	('S', 'Second Player To Move'),
	('W', 'First Player Wins'),
	('L', 'Second Player Wins'),
	('D', 'Draw')
)

# size of the board
BOARD_SIZE = 3


# a custom manager for the Game class.
class GameQuerySet(models.QuerySet):
	def games_for_user(self, user):

		# this code will work as a 'and' operator so use 'Q'
		return self.filter (
			Q(first_player=user) | Q(second_player=user)
		)

	def active(self):
		return self.filter(
			Q(status='F') | Q(status='S')
		)


class Game(models.Model):
	# one to many fields, User comes already in django
	# User is related to first player of game and so on
	first_player = models.ForeignKey(User, related_name="games_first_player", on_delete=models.CASCADE)
	second_player = models.ForeignKey(User, related_name="games_second_player", on_delete=models.CASCADE)

	start_time = models.DateTimeField(auto_now_add=True)
	last_active = models.DateTimeField(auto_now=True)

# we can add choices=___ which will give a drop-down menu
	status = models.CharField(max_length=1, default='F',
		choices=GAME_STATUS_CHOICES)

# overiding the objects manager of this class with GameQuerySet as a manager.
	objects = GameQuerySet.as_manager()

# editing the way strings are shown
	def __str__(self):
		return "{0} vs {1}".format(
			self.first_player, self.second_player)

	# this method of the model gives the url that is associated with this class model
	# now i can ask the instance official url by calling this method which will use reverse to construct correct url
	def get_absolute_url(self):
		return reverse('gameplay_detail', args=[self.id])

	def board(self):
		# board contains three other lists each has three elements
		# initially we are giving the value None
		board = [[None for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]

		for move in self.move_set.all():
			board[move.y][move.x] = move
		return board

	def is_users_move(self, user):
		return (user == self.first_player and self.status == 'F') or\
			(user == self.second_player and self.status == 'S')

	def new_move(self):
		# return a new Move object with player, game
		if self.status not in 'FS':
			raise ValueError('Cannot make move on finished game.')
		return Move(
				game=self,
				by_first_player=self.status == 'F'
			)

	def update_after_move(self, move):
		self.status = self._get_game_status_after_move(move)

	def _get_game_status_after_move(self, move):
		x, y = move.x, move.y
		board = self.board()

		if (board[y][0] == board[y][1] == board[y][2]) or\
			board[x][0] == board[x][1] == board[x][2] or\
			board[0][0] == board[1][1] == board[2][2] or\
			board[2][0] == board[1][1] == board[2][0]:

			return 'W' if move.by_first_player else 'L'
		if self.move_set.count() >= BOARD_SIZE**2:
			return 'D'
		return 'S' if self.status == 'F' else 'F'


class Move(models.Model):
	# storing the moves and validating using the in-built validators
	# MinValue is for 0 as min value and max value is 2 otherwise errors are raised
	# these validations which check form has valid values 
	x = models.IntegerField(
			validators=[MinValueValidator(0), MaxValueValidator(BOARD_SIZE-1)]
		)
	y = models.IntegerField(
			validators=[MinValueValidator(0), MaxValueValidator(BOARD_SIZE-1)]
		)

	# player can comment on every move
	comment = models.CharField(max_length=300, blank=True)

	'''editable=False means we cannot edit it so these won't show up
		in the form, we can do it by putting them in the exclude list
		but this can be done here too.
	'''

	# who made the move, first or second
	by_first_player = models.BooleanField(default=True, editable=False)

	# foreignkey takes on_delete argument, which deletes the all the moves after 
	# game gets deleted
	game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE, editable=False)

	def __eq__(self, other):
		if other is None:
			return False
		return other.by_first_player == self.by_first_player

	def save(self, *args, **kwargs):
		super(Move, self).save(*args, **kwargs)
		self.game.update_after_move(self)
		self.game.save()
