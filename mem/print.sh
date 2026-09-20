#!/bin/bash
function catfootprint
{
    /var/jb/var/root/footprint --swapped --wired -a -j tmp/log/footprint_${1}.json > /dev/null 2>&1
}

# shellcheck disable=SC2120
function catargs
{
    # Wait for run.sh to create the directory
    sleep 1
    j=1
    while true
    do
        catfootprint ${j}
        sleep 3
        j=$((j+1))
    done

}

catargs
