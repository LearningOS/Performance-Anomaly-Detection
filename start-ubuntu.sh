docker run --rm -it \
    -v $(cd `dirname $0`; pwd):/root/project \
    --cpus=1 \
    --memory=4g \
    --memory-swap=4g \
    --device-read-bps /dev/sda:100mb \
    --device-write-bps /dev/sda:100mb \
    --device-read-iops /dev/sda:1000 \
    --device-write-iops /dev/sda:1000 \
    --privileged \
    --name exp \
    perf_exp bash
