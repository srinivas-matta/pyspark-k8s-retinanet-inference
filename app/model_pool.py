from keras_retinanet import models
from pyspark import SparkFiles

class ModelPool:
    model = None

    @staticmethod
    def __init__():
        print("init , model :", ModelPool.model)

    @staticmethod
    def get_model(model_name):
        print("")
        print(" model_map : ", ModelPool.model)
        if  ModelPool.model is None:
            model_path = SparkFiles.get(model_name)
            model = models.load_model(model_path, backbone_name='resnet50')
            ModelPool.model = model

        return ModelPool.model