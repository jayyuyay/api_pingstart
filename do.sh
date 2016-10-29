#!/usr/bin/env bash
start() {
    python api_pingstart_index.py > gp_api.log 2>&1 &
    echo "==========start===========";
}

stop() {
    ps -ef | grep 'python api_pingstart_index.py' | awk -F " " '{print $2}'| xargs kill -9
    echo "===========stop============";
}

restart() {
    ps -ef | grep 'python api_pingstart_index.py' | awk -F " " '{print $2}'| xargs kill -9
    python api_pingstart_index.py > gp_api.log 2>&1 &
    echo "===========restart============";
}
case "$1" in
    'start')
        start
        ;;
    'stop')
        stop
        ;;
    'restart')
        restart
        ;;
    *)
    echo "usage: $0 {start|stop|restart}"
    exit 1
        ;;
    esac
