# shortcut commands for me to speed up development

delete_all() {
    echo "Deleting all pods"
    kubectl delete pods --all
    echo "Deleting all deployments"
    kubectl delete deployments --all
    echo "Deleting all services"
    kubectl delete services --all
}

deploy_cluster() {
    echo "Deploying cluster"
    kubectl apply -f ./k8s/zookeeper-deployment.yaml
    kubectl apply -f ./k8s/zookeeper-service.yaml
    kubectl apply -f ./k8s/kafka-deployment.yaml
    kubectl apply -f ./k8s/kafka-service.yaml
    kubectl apply -f ./k8s/neo4j-deployment.yaml
    kubectl apply -f ./k8s/neo4j-service.yaml
    kubectl apply -f ./k8s/elasticsearch-deployment.yaml
    kubectl apply -f ./k8s/elasticsearch-service.yaml
    kubectl apply -f ./k8s/producer-app-deployment.yaml
}


build_local_images() {
    echo "Building local images"
    docker build -t lamayai/producer-app:latest -f Dockerfile-producer .
    docker build -t lamayai/consumer-app:latest -f Dockerfile-consumer .
}

if [ "$1" == "delete_all" ]; then
    delete_all
    exit 0
elif [ "$1" == "deploy_cluster" ]; then
    deploy_cluster
    exit 0
elif [ "$1" == "build_local_images" ]; then
    build_local_images
    exit 0
else
    echo "Usage: dev.sh [delete_all|deploy_cluster]"
    exit 1
fi