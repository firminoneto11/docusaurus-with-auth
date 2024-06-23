front:
	yarn create docusaurus

compose-dev-up:
	docker compose -f ./build/development/docker-compose.yaml up -d

compose-dev-down:
	docker compose -f ./build/development/docker-compose.yaml down

dev:
	export WATCHFILES_IGNORE_PERMISSION_DENIED=1
	uvicorn --port 8000 --reload src.interface.api.rest.asgi:app
