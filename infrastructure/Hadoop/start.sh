#!/bin/bash
source .env
echo "the total number of datanode is: $NBR_DATANODE"

start_slave_number(){
  for arg in "$@"
  do
    echo "start hadoop-slave$arg container..."
    docker start hadoop-slave"$arg"
  done
}
start_all_slave(){
  i=1
    while [ $i -le $NBR_DATANODE ]
    do
      echo "start hadoop-slave$i container..."
	    docker start hadoop-slave$i
	    ((i++))
    done| tqdm --total "$NBR_DATANODE"
}

start_master(){
  echo "start hadoop-master container..."
	docker start $MASTER_NAME
}

if [ $# = 0 ]
then
	echo "Please specify what you want to do in params"
	exit 1
fi
params=$1

case $params in

  master)
    start_master
    ;;

  start_all)
    start_master
    start_all_slave
    ;;

  slave)
    p=("$@")
    start_slave_number "${p[@]:1}"
    ;;

  all_slave)
    start_all_slave
    ;;

  *)
    echo -n "unknown what you want"
    ;;
esac