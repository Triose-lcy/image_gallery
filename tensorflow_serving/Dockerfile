FROM tensorflow/serving:1.12.0

COPY ./models/ /models/

EXPOSE 8500
EXPOSE 8501

ENTRYPOINT tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=ssd --model_base_path=/models

# Build command: docker build -t triose/tfs_ssd:v1 . 
# Docker Image is uploaded to docker hub.
# To access this image, use: docker pull triose/tfs_ssd:v1

