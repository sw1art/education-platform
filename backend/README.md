docker-compose -f docker-compose-local.yaml up -d --build
docker-compose exec backend alembic init -t async alembic
docker-compose -f docker-compose-local.yaml exec backend alembic init -t async alembic

