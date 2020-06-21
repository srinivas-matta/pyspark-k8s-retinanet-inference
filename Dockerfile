from gcr.io/spark-operator/spark-py:v2.4.5

RUN apt-get update \
    && apt-get install -y curl

RUN apt-get install -y libopencv-dev python-opencv
RUN pip install --upgrade pip
RUN pip install py4j
RUN pip install Cython
RUN pip install numpy
RUN pip install kafka-python==1.4.7
RUN pip install keras-retinanet==0.5.0
RUN pip install opencv-python==4.1.1.26
RUN pip install Pillow==6.2.2
RUN pip install keras==2.2.5
RUN pip install keras-resnet==0.1.0
RUN pip install six
RUN pip install scipy
RUN pip install progressbar2
RUN pip install tensorflow==1.15.0


RUN mkdir /mnt/input-images
RUN mkdir /mnt/output-images

RUN chmod 777 -R /mnt/input-images
RUN chmod 777 -R /mnt/output-images

COPY ./app  /app
COPY ./model/resnet50_coco_best_v2.1.0.h5  /app

ENV PYTHONPATH "${PYTHONPATH}:/"





