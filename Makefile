
run: 
	CASSANDRA_PASSWORD=${CASSANDRA_PASSWORD} python3 -m src

test: clear_db lint integration_tests service_tests sonar

clear_db:
	CASSANDRA_PASSWORD=${CASSANDRA_PASSWORD} python src/config/scylla.py

lint:
	flakeheaven lint src/ tests/
	
integration_tests:
	CASSANDRA_PASSWORD=${CASSANDRA_PASSWORD} PYTHONPATH=. python3 -m pytest -x --junitxml=report_integration_tests.xml --cov=src --cov-config=.coveragerc --cov-report=xml:coverage.xml tests/integration/

service_tests:
	API_SERVER=localhost API_PORT=8000 PYTHONPATH=. pytest --pspec --verbose --color=yes --junitxml=report_service_tests.xml tests/service/auth/


sonar:
	sonar-scanner \
		-Dsonar.projectKey=todo \
		-Dsonar.sources=. \
		-Dsonar.host.url=http://10.2.0.110:9000 \
		-Dsonar.token=${SONAR_TOKEN} \
		-Dsonar.python.coverage.reportPaths=coverage.xml \
		-Dsonar.coverage.exclusions=tests/**,**/router.py,**/src/presentation/**,**/src/models/**,**/src/handler/**,**/src/config/**,**/src/*.py,tailwind.config.js

poetry:
	poetry lock
	poetry install

tailwind:
	tailwindcss -i src/presentation/static/css/main.css -o src/presentation/static/css/main.tailwind.min.css --minify --watch