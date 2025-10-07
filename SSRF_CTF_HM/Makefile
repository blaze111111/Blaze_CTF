APP=ssrf_ctf
PORT_HOST=8081
PORT_CONTAINER=8080
start:
	 docker run --rm -d --name $(CONTAINER) -p $(PORT_HOST):$(PORT_CONTAINER) $(APP)

build:
	docker build -t $(APP) .

run:
	docker run --rm -p 8080:8080 $(APP)

# public tests only
test:
	python -m pytest tests/test_usability.py -q

# local judge (only if hidden_tests are present locally)
securitytest:
	python -m pytest hidden_tests/hidden_security.py -q && cat hidden_tests/flag.txt
