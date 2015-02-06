.PHONY: clean
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;

.PHONY: pep8
pep8:
	@flake8 . --ignore=F403,F401

.PHONY: test
test:
	@export APP_ENV=test && python -m unittest discover

.PHONY: coverage
coverage:
	@export APP_ENV=test && coverage run --source=. -m unittest discover
	@coverage report
