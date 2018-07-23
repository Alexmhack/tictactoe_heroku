from django.urls import path

from .views import game_detail, make_move

urlpatterns = [
	path('detail/<int:id>/', game_detail, name='gameplay_detail'),
	path('make-move/<int:id>/', make_move, name='gameplay_make_move'),
	
]