#!/bin/bash

source .env
HADOOP_TAG=2.7.2-debian
echo "delete and create the new netwok with the same name"
sudo docker network rm hadoop
sudo docker network create --driver=bridge hadoop
# the default node number is 3
N=${1:-3}
echo "the number of node is $N"

# start hadoop master container

sudo docker rm -f hadoop-master &> /dev/null
echo "start hadoop-master container..."
sudo docker run -itd \
                --net=hadoop \
                -p 50070:50070 \
                -p 8088:8088 \
		            -p 7077:7077 \
		            -p 16010:16010 \
		            -v "$DIR_DATA":/data \
		            -v "$DIR_CODE":/code \
                --name hadoop-master \
                --hostname hadoop-master \
                spark-hadoop:"$HADOOP_TAG"-"$N"-datanode

# start hadoop slave container
i=1
while [ $i -le "$N" ]
do
	sudo docker rm -f hadoop-slave$i &> /dev/null
	echo "start hadoop-slave$i container..."
	port=$(( 8040 + $i ))
	sudo docker run -itd \
			-p $port:8042 \
	    --net=hadoop \
	    --name hadoop-slave$i \
	    --hostname hadoop-slave$i \
	    spark-hadoop:"$HADOOP_TAG"-"$N"-datanode &> /dev/null
	i=$(( $i + 1 ))
done| tqdm --total "$N"
sudo docker exec -it hadoop-master bash