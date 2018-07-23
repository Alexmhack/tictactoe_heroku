from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Move

# a ModelForm class has to have a exclude or include list but we can leave it empty
class MoveForm(ModelForm):
	class Meta:
		# model = Move means this form is based on the Move model
		# it will show all the fields from the Move model
		model = Move
		exclude = []

	# ModelForm has a clean method, we are overriding it
	def clean(self):
		# if the cleaned_data has x and y values it will be returned
		# else None will be returned
		x = self.cleaned_data.get('x')
		y = self.cleaned_data.get('y')

		game = self.instance.game

		try:
			# here we check it those values are not None
			if game.board()[y][x] is not None:
				raise ValidationError('square is not empty')
		except IndexError:
			raise ValidationError('Invalid coordinates')

		# clean return a cleaned_data so we are returning it
		return self.cleaned_data