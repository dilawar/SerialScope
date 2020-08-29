all : arduino
	python3 -m SerialScope

arduino:
	cd ./Arduino && make upload

test :
	python3 -m SerialScope

dist :
	python3 setup.py sdist


upload :  dist
	twine check dist/*
	twine upload dist/*
