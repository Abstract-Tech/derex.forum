#!/bin/sh -e

case "$@" in
    sh)
        exec "$@"
        ;;

    *)
        export MONGOHQ_URL="mongodb://$MONGODB_AUTH$MONGODB_HOST:$MONGODB_PORT/$MONGODB_DB"

        echo "Waiting for mongodb and elasticsearch..."
        dockerize -wait tcp://$MONGODB_HOST:$MONGODB_PORT -wait $SEARCH_SERVER/content -wait-retry-interval 5s -timeout 600s

        exec "$@"
esac
