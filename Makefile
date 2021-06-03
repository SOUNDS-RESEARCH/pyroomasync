 .PHONY: install lint

install:
	@python install -r requirements.txt

lint:
	@flake8

test:
	@pytest tests/
