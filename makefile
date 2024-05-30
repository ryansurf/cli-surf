.PHONY: run test post_test

run:
	cd src && python3 server.py

test:
	pytest -s -x --cov=src -vv

post_test:
	coverage html
