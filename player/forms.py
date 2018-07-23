from django.forms import ModelForm

from .models import Invitation


class InvitationForm(ModelForm):
	# this is common, you can tell django in meta class about the 
	# model and other things
	class Meta:
		# model here is our Invitation we imported at top
		"""
		django forms represent a html form and a ModelForm class creates
		a form based on the fields in the model.
		"""
		model = Invitation

		# we don't want these fields to show in our form page
		exclude = ('from_user', 'timestamp')