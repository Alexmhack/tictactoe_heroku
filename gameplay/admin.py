from django.contrib import admin

from .models import Move, Game


# registering for the game class 
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
	list_display = ('id', 'first_player', "second_player", "status")

# editable list view, here comma after '' is necessary
# which says this is tuple and not a string in ()
	list_editable = ('status',)

# links which can be clicked.
	list_display_links = ("first_player",)


admin.site.register(Move)