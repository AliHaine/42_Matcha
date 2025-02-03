cd "$(dirname "$0")"

docker-compose -f ./database/docker-compose.yml up -d