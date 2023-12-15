
run: 
	SERVER_MONGO_URL=mongodb://root:example@localhost:27017 python3 -m src

test: integration_tests

integration_tests:
	SERVER_MONGO_URL=mongodb://root:example@localhost:27017 PYTHONPATH=. python3 -m pytest -x --junitxml=report_integration_tests.xml --cov=src --cov-config=.coveragerc --cov-report=xml:integration_coverage.xml tests/integration/

lint:
	flakeheaven lint src/ tests/

sonar:
	sonar-scanner \
		-Dsonar.projectKey=Todo-Collab \
		-Dsonar.sources=. \
		-Dsonar.host.url=http://10.2.0.104:9000 \
		-Dsonar.token=${SONAR_TOKEN} \
		-Dsonar.python.coverage.reportPaths=integration_coverage.xml \
		-Dsonar.coverage.exclusions=tests/**,**/router.py,**/src/presentation/**,**/src/models/**,**/src/handler/**,**/src/config/**,**/src/*.py,**/src/logic/**