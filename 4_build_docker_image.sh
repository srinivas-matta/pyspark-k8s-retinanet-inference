eval $(minikube docker-env)

docker build -t localhost:5000/spark_inference_image:1.0  .

docker push localhost:5000/spark_inference_image:1.0

