all : arduino
	python3 ./main.py

arduino:
	cd ./SignalGenerator && make upload
