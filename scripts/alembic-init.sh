# REVIEW: UPDATE IT

!/bin/bash
if [ "$(ls -d ./migrations)" ]; then
    echo "Migrations exist"
    docker exec -it golfin-miniapp-backend alembic current >/dev/null
    docker exec -it golfin-miniapp-backend alembic upgrade head >/dev/null
    docker exec -it golfin-miniapp-backend alembic current
else
    echo "Migrations does not exist"
    docker exec -it golfin-miniapp-backend alembic init migrations >/dev/null
    sleep 3
    docker exec -it golfin-miniapp-backend cat ./env_ref.py > ./migrations/env.py >/dev/null
    sleep 3
    # docker exec -it golfin-miniapp-backend cat ./alembic_ref.ini > ./alembic.ini >/dev/null
    docker exec -it golfin-miniapp-backend alembic current >/dev/null
    docker exec -it golfin-miniapp-backend alembic revision --autogenerate -m "init" >/dev/null
    docker exec -it golfin-miniapp-backend alembic upgrade head >/dev/null
    docker exec -it golfin-miniapp-backend alembic current
fi


# if [ "$(ls -d ./migrations/versions)" ]; then
#     latest_revision=$(ls -t /migrations/versions | head -n 1) | grep revision | awk '{print $2}'
#     echo $latest_revision
# else
#     echo "Directory does not exist"
# fi
