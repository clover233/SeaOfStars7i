#!/bin/bash

PASSWORD='alpine'
IP='127.0.0.1'
PORT='2222'
USER='root'
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ "${1:-}" = "stop" ]; then
    sshpass -p "${PASSWORD}" ssh -o StrictHostKeyChecking=no -p "${PORT}" "${USER}@${IP}" \
        'if [ -f ~/tmp/run.pid ]; then kill "$(cat ~/tmp/run.pid)" 2>/dev/null || true; rm -f ~/tmp/run.pid; fi'
    exit $?
fi

sshpass -p "${PASSWORD}" ssh -o StrictHostKeyChecking=no -p "${PORT}" "${USER}@${IP}" "mkdir -p ~/tmp/log"
sshpass -p "${PASSWORD}" scp -o StrictHostKeyChecking=no -P "${PORT}" "${SCRIPT_DIR}/run.sh" "${USER}@${IP}:~/tmp/"
sshpass -p "${PASSWORD}" ssh -o StrictHostKeyChecking=no -p "${PORT}" "${USER}@${IP}" \
    'if [ -f ~/tmp/run.pid ]; then kill "$(cat ~/tmp/run.pid)" 2>/dev/null || true; rm -f ~/tmp/run.pid; fi'

exec sshpass -p "${PASSWORD}" ssh -o StrictHostKeyChecking=no -p "${PORT}" "${USER}@${IP}" "bash ~/tmp/run.sh"
