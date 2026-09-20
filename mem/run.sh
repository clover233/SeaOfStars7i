#!/bin/bash
function catzprint
{
    time=$(date "+%Y-%m-%d %H:%M:%S")
    echo ${time} >> tmp\/log\/sysctllog_${1}
    zprint >> tmp/log/zprint_${1}
}

function catvmstat
{
    time=$(date "+%Y-%m-%d %H:%M:%S")
    echo ${time} >> tmp\/log\/vmstatlog_${1}
    vm_stat >> tmp\/log\/vmstatlog_${1}
}

function catsys
{
    time=$(date "+%Y-%m-%d %H:%M:%S")
    echo ${time} >> tmp\/log\/sysctllog_${1}
    /var/jb/usr/sbin/sysctl -a >> tmp\/log\/sysctllog_${1}
}

# shellcheck disable=SC2120
function catargs
{
    rm -rf tmp/log/
    mkdir tmp/log/
    i=1
    while true
    do
        catzprint ${i}
        catvmstat ${i}
        catsys ${i}
        sleep 5
        i=$((i+1))
    done

}

catargs
