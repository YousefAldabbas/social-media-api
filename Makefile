run:
	python manage.py runserver

format:
	black . && isort . 