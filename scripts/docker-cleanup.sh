!/bin/bash

docker-compose down
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
# すべてのイメージを削除
docker rmi $(docker images -q)
# すべてのボリュームを削除
docker volume rm $(docker volume ls -q)
# すべてのネットワークを削除
docker network rm $(docker network ls -q)
# ビルドキャッシュを削除
docker builder prune -a
# システム全体をクリーンアップ
docker system prune -a --volumes