from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
import grpc
import tensorflow as tf
import numpy as np
import cv2


def resize_inference(img, server_url, dest_size=(300, 300)):
    img_resized = cv2.resize(img, (300, 300))
    return inference(img_resized, server_url)


def inference(img_resized, server_url):
    # Request.
    channel = grpc.insecure_channel(server_url)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    request = predict_pb2.PredictRequest()
    request.model_spec.name = "ssd"  # 模型名称，启动容器命令的model_name参数
    request.model_spec.signature_name = "predict"  # 签名名称，刚才叫你记下来的
    # "input_1"是你导出模型时设置的输入名称，刚才叫你记下来的
    request.inputs["inputs"].CopyFrom(
        tf.make_tensor_proto(img_resized, shape=[1, ] + list(img_resized.shape)))
    response = stub.Predict(request, 5.0)  # 5 secs timeout
    return np.asarray(response.outputs["outputs"].float_val).reshape((-1, 200, 6))