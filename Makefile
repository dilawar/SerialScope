all : arduino
	python3 -m SerialScope

arduino:
	cd ./SignalGenerator && make upload

test :
	python3 -m SerialScope
