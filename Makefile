all : arduino
	python3 -m SerialScope

arduino:
	cd ./arduino && make upload

test :
	python3 -m SerialScope

upload : 
	python3 setup.py sdist
	python3 -m twine check dist/*
	python3 -m twine upload dist/*
