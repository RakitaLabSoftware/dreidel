install:
	conda env create -f enviroment.yml && conda activate dreidel && python3 -m pip install -e . 
run:
	python main.py 
test:
	pytest