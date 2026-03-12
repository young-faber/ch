dev:
	./manage.py runserver
dev-as:
	uvicorn chess.asgi:application --reload

