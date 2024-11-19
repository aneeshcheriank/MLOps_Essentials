venv:
	python -m venv ~/.venv

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=TSP test_TSP.py

lint:
	pylint --disable=R,C,E1120 *.py

format:
	black *.py