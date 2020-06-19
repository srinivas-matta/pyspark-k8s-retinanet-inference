eval $(minikube docker-env)

kubectl delete  -f k8s/spark_inference.yaml

kubectl create  -f k8s/spark_inference.yaml

