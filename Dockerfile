FROM python:3.11-slim
WORKDIR /usr/app/comfyui-rest-api

# Install dependencies
RUN apt-get update && apt install -y git

# Download and install ComfyUI and its dependencies
RUN git clone https://github.com/comfyanonymous/ComfyUI.git
RUN pip install -r ./ComfyUI/requirements.txt

# Install API dependencies
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

# Copy code at last
COPY ./src ./src