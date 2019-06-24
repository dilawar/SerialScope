all : arduino
	python3 -m SerialScope

arduino:
	cd ./SerialScopeArduino && make upload

test :
	python3 -m SerialScope

upload : 
	python3 setup.py sdist
	twine check dist/*
	twine upload dist/*
