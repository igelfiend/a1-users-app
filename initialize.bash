docker container stop postgres_db
docker-compose down --rmi all --volumes
docker-compose build
docker-compose up -d db
sleep 1
docker-compose run a1-users-app alembic -c ./app/alembic.ini upgrade head
