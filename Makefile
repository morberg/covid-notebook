.PHONY: all
all: html charts

html: lag header.html covid-sweden.html footer.html
	cat header.html covid-sweden.html footer.html > covid.html
    cat header.html excess-mortality.html footer.html > excess.html

lag:
	jupyter-nbconvert --execute --ExecutePreprocessor.kernel_name=python3 --to html \
		--template basic --no-input --no-prompt covid-sweden.ipynb

excess:
	jupyter-nbconvert --execute --ExecutePreprocessor.kernel_name=python3 --to html \
		--template basic --no-input --no-prompt excess-mortality.ipynb


.PHONY: charts
charts:
	python generate-html-charts.py