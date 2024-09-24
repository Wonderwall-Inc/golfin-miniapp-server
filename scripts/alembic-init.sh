# REVIEW: UPDATE IT

!/bin/bash
if [ "$(ls -d migrations)" ]; then
    echo "Migrations exist"
    docker exec -it golfin-miniapp-backend alembic current
    docker exec -it golfin-miniapp-backend alembic upgrade head
    docker exec -it golfin-miniapp-backend alembic current
else
    echo "Migrations does not exist"
    docker exec -it golfin-miniapp-backend alembic init migrations
    docker exec -it golfin-miniapp-backend cat env_dev_ref.py > migrations/env.py
    # docker exec -it golfin-miniapp-backend cat ./alembic_ref.ini > ./alembic.ini >/dev/null
    docker exec -it golfin-miniapp-backend alembic current
    docker exec -it golfin-miniapp-backend alembic revision --autogenerate -m "init" 
    docker exec -it golfin-miniapp-backend alembic upgrade head
    docker exec -it golfin-miniapp-backend alembic current
fi