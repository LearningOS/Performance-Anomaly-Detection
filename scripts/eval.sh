#!/usr/bin/env bash

#PYTHONPATH=. python scripts/eval.py \
#    --data \
#        log/pgbench.data.pkl \
#        log/nginx.data.pkl \
#        log/mcperf.set.data.pkl \
#        log/redis.set.data.pkl \
#    --normal \
#        log/pgbench.normal.pkl \
#        log/nginx.normal.pkl \
#        log/mcperf.set.normal.pkl \
#        log/redis.set.normal.pkl \
#    --anomaly \
#        log/pgbench.anomaly.pkl \
#        log/nginx.anomaly.pkl \
#        log/mcperf.set.anomaly.pkl \
#        log/redis.set.anomaly.pkl


PYTHONPATH=. python scripts/eval.py \
    --data \
        log/x264.data.pkl \
        log/video-cpu-usage.data.pkl \
        log/compress-gzip.data.pkl \
        log/idle.data.pkl \
    --normal \
        log/x264.normal.pkl \
        log/video-cpu-usage.normal.pkl \
        log/compress-gzip.normal.pkl \
        log/idle.normal.pkl \
    --anomaly \
        log/x264.anomaly.pkl \
        log/video-cpu-usage.anomaly.pkl \
        log/compress-gzip.anomaly.pkl \
        log/idle.anomaly.pkl


#PYTHONPATH=. python scripts/eval.py \
#    --data \
#        log/scikit-learn.data.pkl \
#        log/tensorflow.data.pkl \
#        log/build-linux-kernel.data.pkl \
#        log/blender.data.pkl \
#    --normal \
#        log/scikit-learn.normal.pkl \
#        log/tensorflow.normal.pkl \
#        log/build-linux-kernel.normal.pkl \
#        log/blender.normal.pkl \
#    --anomaly \
#        log/scikit-learn.anomaly.pkl \
#        log/tensorflow.anomaly.pkl \
#        log/build-linux-kernel.anomaly.pkl \
#        log/blender.anomaly.pkl