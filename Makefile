.PHONY: run-server
run-server:
	python manage.py runserver

.PHONY: run-makemigration
run-makemigration:
	python manage.py makemigrations

.PHONY: run-migration
run-migration:
	python manage.py migrate
