# docker_pass

docker build -t app ./app
docker build -t service ./service

# windows
# docker volume create --driver local --opt type=none --opt device=volume --opt o=bind volume

docker swarm init
docker stack deploy -c docker-compose.yml myapp
