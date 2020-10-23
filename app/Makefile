requirements:
	pip3 install -r requirements.txt

env:
	python3 -m venv env

activate:
	(source ./env/bin/activate)

run:
	(gunicorn -b 0.0.0.0:80  routes:app --timeout 200)