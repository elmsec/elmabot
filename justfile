run:
	python -m elmabot

hlogs:
	heroku logs --tail

hstop:
	heroku ps:stop elmabot

hrestart:
	heroku ps:restart elmabot
