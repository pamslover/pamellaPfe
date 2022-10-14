DOCKER_NETWORK = hadoop-net
ENV_FILE = hadoop.env
HADOOP_TAG := 2.7.2-debian
HADOOP_VERSION := 2.7.2

N=${1:-3}

build_image:
	docker build \
		-t spark-hadoop:$(HADOOP_TAG)-$N-datanode \
		--build-arg IMAGE_TAG=$(HADOOP_TAG) \
        --build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
        --build-arg HADOOP_VERSION="2.7.2" .

resize:
	./resize-cluster.sh $N

first_start:
	./restart.sh $N

stop:
	./stop.sh $(ARGS)

start:
	./start.sh $(ARGS)
