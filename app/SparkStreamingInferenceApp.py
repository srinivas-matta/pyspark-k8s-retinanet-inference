import os
import cv2
import numpy as np

from keras_retinanet.utils.colors import label_color
from keras_retinanet.utils.image import read_image_bgr, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BinaryType
from pyspark import TaskContext
from pyspark.sql import SparkSession

if __name__ == '__main__':

    spark = SparkSession.builder.getOrCreate()

    model_path = "/app/resnet50_coco_best_v2.1.0.h5"
    model_name = os.path.basename(model_path)

    print("model_name : ", model_name)

    spark.sparkContext.addFile(model_path)

    spark.sparkContext.addPyFile("/app/model_pool.py")
    print("distributing model file to executor.")

    ImageFields = ["origin", "height", "width", "nChannels", "mode", "data"]
    ImageSchema = StructType([
        StructField(ImageFields[0], StringType(), True),
        StructField(ImageFields[1], IntegerType(), True),
        StructField(ImageFields[2], IntegerType(), True),
        StructField(ImageFields[3], IntegerType(), True),
        StructField(ImageFields[4], IntegerType(), True),
        StructField(ImageFields[5], BinaryType(), True)
    ]
    )

    image_schema = StructType().add("image", ImageSchema)

    image_df = spark.readStream.format("image").schema(image_schema).load("/mnt/input-images")

    labels_to_names = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train',
                       7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign',
                       12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep',
                       19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack',
                       25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis',
                       31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove',
                       36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass',
                       41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple',
                       48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza',
                       54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed',
                       60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote',
                       66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink',
                       72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear',
                       78: 'hair drier', 79: 'toothbrush'}

    def processImg(iterator):

        print("processing image..")
        ctx = TaskContext()
        partition_id = ctx.partitionId()

        from app.model_pool import ModelPool
        model = ModelPool.get_model_for_partition_id( model_name)
        print("partition_id : ", partition_id , "  model : ", model)

        for img_row in iterator:

            row_dict = img_row.asDict()
            filepath =row_dict['origin']
            height = row_dict['height']
            width  = row_dict['width']
            nChannels = row_dict['nChannels']

            import os
            filename = os.path.basename(filepath)
            print("filename", filename)

            data = row_dict['data']
            shape = (height, width, nChannels)
            image_np_array=  np.ndarray(shape, np.uint8, data)
            resized_image , scale = resize_image(image_np_array)

            boxes, scores, labels = model.predict_on_batch(np.expand_dims(resized_image, axis=0))

            for box, score, label in zip(boxes[0], scores[0], labels[0]):
                # scores are sorted so we can break

                if score < float("0.2"):
                    break
                color = label_color(label)
                b = box.astype(int)
                draw_box(resized_image, b, color=color)
                caption = "{} {:.3f}".format(labels_to_names[label], score)
                draw_caption(resized_image, b, caption)

            cv2.imwrite("/mnt/output-images/" + filename, resized_image)


    def process_batch_df(image_df, batch_id):
        print("batch_id : ", batch_id)
        image_df.select("image.height", "image.width", "image.nChannels", "image.mode", "image.origin", "image.data").foreachPartition(processImg)


    query = image_df \
        .writeStream \
        .trigger(processingTime='5 seconds') \
        .foreachBatch(process_batch_df)\
        .start()

    query.awaitTermination()
