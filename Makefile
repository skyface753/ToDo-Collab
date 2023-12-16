
run: 
	SERVER_MONGO_URL=${SERVER_MONGO_URL} python3 -m src

test: lint integration_tests service_tests

lint:
	flakeheaven lint src/ tests/
	
integration_tests:
	SERVER_MONGO_URL=${SERVER_MONGO_URL} PYTHONPATH=. python3 -m pytest -x --junitxml=report_integration_tests.xml --cov=src --cov-config=.coveragerc --cov-report=xml:coverage.xml tests/integration/

service_tests:
	API_SERVER=localhost API_PORT=8000 PYTHONPATH=. pytest --pspec --verbose --color=yes --junitxml=report_service_tests.xml tests/service/


sonar:
	sonar-scanner \
		-Dsonar.projectKey=Todo-Collab \
		-Dsonar.sources=. \
		-Dsonar.host.url=http://10.2.0.104:9000 \
		-Dsonar.token=${SONAR_TOKEN} \
		-Dsonar.python.coverage.reportPaths=coverage.xml \
		-Dsonar.coverage.exclusions=tests/**,**/router.py,**/src/presentation/**,**/src/models/**,**/src/handler/**,**/src/config/**,**/src/*.py