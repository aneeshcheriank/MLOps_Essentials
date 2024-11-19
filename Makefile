venv:
	python -m venv ~/.venv

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=app test_app.py

lint:
	pylint --disable=R,C app.py

format:
	black *.py