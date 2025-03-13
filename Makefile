run:
	./manage.py runserver

test:
	coverage run && coverage report

makemig:
	./manage.py makemigrations

mig:
	./manage.py migrate

static:
	./manage.py collectstatic

super:
	./manage.py createsuperuser

shell:
	./manage.py shell