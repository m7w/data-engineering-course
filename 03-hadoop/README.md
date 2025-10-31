## set environment variables and start dfs and yarn
```sh
. ./env.sh
start-all.sh
```

## STAGE 1
```sh
yarn jar $HADOOP_STREAMING_JAR \
    -files stage1/mapper.py,stage1/combiner.py,stage1/reducer.py,TNVED3.TXT \
    -input /user/max/input \
    -output /user/max/summed \
    -mapper mapper.py \
    -combiner combiner.py \
    -reducer reducer.py
```

## STAGE 2
```sh
yarn jar $HADOOP_STREAMING_JAR \
    -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
    -D stream.num.map.output.key.fields=2 \
    -D mapreduce.partition.keycomparator.options="-k2,2nr" \
    -files stage2/mapper.py,stage2/reducer.py \
    -input /user/max/summed \
    -output /user/max/output \
    -mapper mapper.py \
    -reducer reducer.py
```
