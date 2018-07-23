from django.db import models
from django.contrib.auth.models import User


class Invitation(models.Model):

# fields which will have a set of objects of user class 
# with name = related_name
	from_user = models.ForeignKey(
		User, 
		related_name="Invitation_sent", 
		on_delete=models.CASCADE,
	)
	# verbose_name will be name of field on webpage
	# help_text gives extra details
	to_user = models.ForeignKey(
		User, 
		related_name="invitations_received",
		verbose_name="User to invite",
		help_text="Please select the user for sending invitation.",
		on_delete=models.CASCADE
	)
	
# fields for writing message to be sent to the user
# message is optional so blank is True.
	message = models.CharField(
		max_length=300, blank=True,
		verbose_name="Optional Message",
		help_text="It's always nice to add a friendly message!",
	)

	timestamp = models.DateTimeField(auto_now_add=True)
