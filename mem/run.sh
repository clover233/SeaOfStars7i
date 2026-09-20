#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/log"
PID_FILE="${SCRIPT_DIR}/run.pid"

function cleanup
{
    rm -f "${PID_FILE}"
}

trap 'exit 0' INT TERM HUP
trap cleanup EXIT
echo "$$" > "${PID_FILE}"

function catfootprint
{
    footprint --swapped --wired -a -j "${LOG_DIR}/footprint_${1}.json" > /dev/null 2>&1
}

function catzprint
{
    time=$(date "+%Y-%m-%d %H:%M:%S")
    echo "${time}" >> "${LOG_DIR}/zprint_${1}"
    /usr/bin/zprint >> "${LOG_DIR}/zprint_${1}"
}

function catvmstat
{
    time=$(date "+%Y-%m-%d %H:%M:%S")
    echo "${time}" >> "${LOG_DIR}/vmstatlog_${1}"
    /usr/bin/vm_stat >> "${LOG_DIR}/vmstatlog_${1}"
}

function catsysctl
{
    time=$(date "+%Y-%m-%d %H:%M:%S")
    echo "${time}" >> "${LOG_DIR}/sysctl_${1}"
    /var/jb/usr/sbin/sysctl -a >> "${LOG_DIR}/sysctl_${1}"
}

function catargs
{
    rm -rf "${LOG_DIR}"
    mkdir -p "${LOG_DIR}"
    i=1
    while true
    do
        catvmstat "${i}"
        catsysctl "${i}"
        catzprint "${i}"
        catfootprint "${i}"
        sleep 3
        i=$((i + 1))
    done
}

catargs
