all : arduino
	python3 -m ArduinoScope

arduino:
	cd ./SignalGenerator && make upload

test :
	python3 -m ArduinoScope
