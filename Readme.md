
 ### Deploying Spark on Kubernetes using Sparkoperator    
 Dependencies:    
* Docker     
* Minikube     
* Spark     
    
  
Minikube used to run a single-node Kubernetes cluster locally.    
  
Run these steps in sequential manner,  
  
* Default,  Minikube memory settings are not enough for Spark jobs, need to be increase the memory and cpu cores  
  
   `$ 1_kubernetes_setup.sh `  
  
* Installing sparkoperator    

   `$ 2_install_spark_operator.sh `  
  
* Mounting local file system to minkube. make sure this service is running while spark is running  
  
   `$ 3_mount_data_local_minikube.sh `  
   
* Building docker image for the spark application  
  
   `$ 4_build_docker_image.sh `  
  
* Creating Spark cluster on Kubernetes using sparkoperator  
  
   `$ 5_create_spark_k8s_cluster.sh`  
  
* Deleting pods & resource  
  
   `$ 6_delete_spark_k8s_cluster.sh`    
   
 Note :  
Copy 'resnet50_coco_best_v2.1.0.h5' to 'model' folder.   
  
'resnet50_coco_best_v2.1.0.h5' can be downloaded here : https://github.com/fizyr/keras-retinanet/releases