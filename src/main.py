import base64
import json
import logging
import urllib.request
import urllib.parse
import uuid
import websocket

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict


# Load default logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


def queue_prompt(server_address, client_id, prompt):
    """This function sends a prompt to the ComfyUI server."""

    payload = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(payload).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())


class Payload(BaseModel):  # pylint: disable=too-few-public-methods
    """Payload properties."""

    prompt: Dict = Field(
        title='Prompt',
        description='Workflow in ComfyUI API format.'
    )

class Response(BaseModel):  # pylint: disable=too-few-public-methods
    """Response properties."""

    image: str = Field(
        title='Image',
        description='Generated image.'
    )

# API definition
api_title = 'ComfyUI REST API'
api_version = '0.0.1'
comfyui_server = '127.0.0.1:8188'
client_id = str(uuid.uuid4())
log.info('Start %s API, version %s', api_title, api_version)
app = FastAPI(title=api_title, version=api_version)
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

# Endpoints
@app.post('/prompt', response_model=Response, description='Execute a ComfyUI workflow.')
def prompt(payload: Payload):
    # Create websocket connection to connect to the ComfyUI server
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(comfyui_server, client_id))

    # Send workflow to ComfyUI API
    prompt = payload.prompt
    prompt_id = queue_prompt(comfyui_server, client_id, prompt)['prompt_id']

    # Listen to the websocket connection to retrieve image data
    output_images = {}
    current_node = ""
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['prompt_id'] == prompt_id:
                    if data['node'] is None:
                        break #Execution is done
                    else:
                        current_node = data['node']
        else:
            if current_node == 'save_image_websocket_node':
                images_output = output_images.get(current_node, [])
                images_output.append(out[8:])
                output_images[current_node] = images_output
    
    # Retrieve image and convert it to data URI
    for node_id in output_images:
        for image_data in output_images[node_id]:
            prefix = 'data:image/png;base64,'
            image_uri = prefix + base64.b64encode(image_data).decode('utf8')

    response = { 'image': image_uri }
    return JSONResponse(content=response, status_code=200)
