all : arduino
	python3 -m SerialScope

arduino:
	cd ./arduino && make upload

test :
	python3 -m SerialScope
