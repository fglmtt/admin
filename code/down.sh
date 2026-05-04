#!/bin/bash

run() {
    local label=$1
    shift
    echo -n "${label}... "
    if output=$("$@" 2>&1); then
        echo "OK"
    else
        echo "FAILED"
        echo "$output"
    fi
}

echo "Containers:"
for c in firewall client web; do
    if podman container exists "$c"; then
        run "  Removing $c" podman rm -f -t 0 "$c"
    else
        echo "  Removing $c... SKIPPED (not present)"
    fi
done

echo
echo "Networks:"
for n in external internal; do
    if podman network exists "$n"; then
        run "  Removing $n" podman network rm "$n"
    else
        echo "  Removing $n... SKIPPED (not present)"
    fi
done
