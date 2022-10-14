#!/bin/bash
source .env
echo "the total number of datanode is: $NBR_DATANODE"

stop_slave_number(){
  for arg in "$@"
  do
    echo "stop hadoop-slave$arg container..."
    docker stop hadoop-slave"$arg"
  done
}
stop_all_slave(){
  i=1
    while [ $i -le $NBR_DATANODE ]
    do
      echo "stop hadoop-slave$i container..."
	    docker stop hadoop-slave$i
	    ((i++))
    done |tqdm --total "$NBR_DATANODE"
}

stop_master(){
  echo "stop hadoop-master container..."
	docker stop $MASTER_NAME
}

if [ $# = 0 ]
then
	echo "Please specify what you want to do in params"
	exit 1
fi
params=$1

case $params in

  master)
    stop_master
    ;;
  stop_all)
    stop_master
    stop_all_slave
    ;;
  slave)
    p=("$@")
    stop_slave_number "${p[@]:1}"
    ;;

  all_slave)
    stop_all_slave
    ;;

  *)
    echo -n "unknown what you want"
    ;;
esac