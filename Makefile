.PHONY: help docker-rebuild docker-stop docker-logs test

help:
	@echo "Available commands:"
	@echo "  make help           - Show this help message"
	@echo "  make docker-rebuild - Rebuild and restart the Docker container"
	@echo "  make docker-stop    - Stop and remove the Docker container"
	@echo "  make docker-logs    - View container logs in follow mode"
	@echo "  make test          - Run the test suite"

docker-rebuild:
	./scripts/docker-rebuild.sh

docker-stop:
	docker rm -f md-publish-container 2>/dev/null || true

docker-logs:
	docker logs -f md-publish-container

test:
	uv run -m pytest -v 