init:
	docker network create internal-1 || echo "Network already initialized"