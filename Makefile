all : arduino
	python3 ./main.py

arduino:
	cd ./SignalGenerator && make upload

test :
	python3 -m ArduinoScope
