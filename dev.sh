# shortcut commands for me to speed up development

delete_all() {
    echo "Deleting all pods"
    kubectl delete pods --all
    echo "Deleting all deployments"
    kubectl delete deployments --all
    echo "Deleting all services"
    kubectl delete services --all
    echo "Deleting all configmaps"
    kubectl delete configmaps --all
    echo "Deleting all secrets"
    kubectl delete secrets --all
}

deploy_cluster() {
    echo "============= Deploying local cluster ============="

    echo "Creating persistent volumes"
    kubectl apply -f ./k8s/neo4j-persistent-volume.yaml
    kubectl apply -f ./k8s/neo4j-persistent-volume-claim.yaml

    echo "Creating configmaps"
    kubectl apply -f ./k8s/cluster_config.yaml

    echo "Creating secrets"
    kubectl apply -f ./k8s/cluster_secrets.yaml

    echo "Creating deployments and services"
    kubectl apply -f ./k8s/zookeeper-deployment.yaml
    sleep 5
    kubectl apply -f ./k8s/zookeeper-service.yaml
    sleep 5
    kubectl apply -f ./k8s/kafka-deployment.yaml
    sleep 5
    kubectl apply -f ./k8s/kafka-service.yaml
    sleep 5
    kubectl apply -f ./k8s/neo4j-deployment.yaml
    sleep 5
    kubectl apply -f ./k8s/neo4j-service.yaml
    sleep 5
    kubectl apply -f ./k8s/elasticsearch-deployment.yaml
    sleep 5
    kubectl apply -f ./k8s/elasticsearch-service.yaml
    sleep 5
    kubectl apply -f ./k8s/producer-app-deployment.yaml
    sleep 5
    kubectl apply -f ./k8s/consumer-app-deployment.yaml
}

build_local_images() {
    echo "Building local images"
    docker build --no-cache -t lamayai/producer-app:latest -f Dockerfile-producer .
    docker build --no-cache -t lamayai/consumer-app:latest -f Dockerfile-consumer .
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
    echo "Usage: dev.sh [delete_all|deploy_cluster|build_local_images]"
    exit 1
fi