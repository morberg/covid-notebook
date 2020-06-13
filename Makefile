.PHONY: all
all: html charts

html: lag header.html covid-sweden.html footer.html
	cat header.html covid-sweden.html footer.html > covid.html

lag:
	jupyter-nbconvert --execute --ExecutePreprocessor.kernel_name=python3 --to html \
		--template basic --no-input --no-prompt covid-sweden.ipynb

.PHONY: charts
charts:
	python generate-html-charts.py