from gcr.io/spark-operator/spark-py:v2.4.5

RUN apt-get update \
    && apt-get install -y curl

RUN apt-get install -y libopencv-dev python-opencv
RUN pip install py4j
RUN pip install Cython
RUN pip install numpy
RUN pip install kafka-python==1.4.7
RUN pip install keras-retinanet==0.5.0
RUN pip install opencv-python==4.1.1.26
RUN pip install Pillow==6.2.1
RUN pip install tensorboard==1.14.0
RUN pip install tensorflow==1.14.0


RUN mkdir /mnt/input-images
RUN mkdir /mnt/output-images

RUN chmod 777 -R /mnt/input-images
RUN chmod 777 -R /mnt/output-images

COPY ./app  /app
COPY ./model/resnet50_coco_best_v2.1.0.h5  /app

ENV PYTHONPATH "${PYTHONPATH}:/"

#docker build -t spark_inference_image:v1  .
#docker run -v $(pwd)/app:/app -v $(pwd)/input_raw_images:/mnt/input-images -v $(pwd)/output-images:/mnt/output-images  --entrypoint "sh" spark_inference_image:v1
#spark-submit --master local SparkKerasTest.py



