from imageai.Detection.Custom import DetectionModelTrainer

# Initialize the model trainer and set it to YOLO (YOLOv3 is optional)
train = DetectionModelTrainer()
train.setModelTypeAsYOLOv3()

# Choose the name of your directory
d_name = "tires"
train.setDataDirectory(data_directory=d_name)
train.setTrainConfig(object_names_array=[d_name], batch_size=4, num_experiments=203)
train.trainModel()
