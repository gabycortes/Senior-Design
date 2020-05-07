from imageai.Detection.Custom import DetectionModelTrainer

train = DetectionModelTrainer()
train.setModelTypeAsYOLOv3()
# put your director name
d_name = "tires"
train.setDataDirectory(data_directory=d_name)
train.setTrainConfig(object_names_array=[d_name], batch_size=4, num_experiments=203)
train.trainModel()
