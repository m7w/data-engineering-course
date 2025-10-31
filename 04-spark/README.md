## set environment variables and start dfs and yarn
```sh
. ./env.sh
start-all.sh
```

## submit spark job
```sh
spark-submit --master yarn --conf spark.local.dir="$HOME/tmp/spark-temp" job.py
```
