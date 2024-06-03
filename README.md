# ComfyUI-FastAPI

Boilerplate code to create a thin REST API layer on top of ComfyUI with FastAPI.

## Getting started

Place a model safetensors file in the folder `./models/checkpoints`, then run the following commands:

```sh
docker compose build
docker compose up
```

You can access the Swagger of the API at [http://localhost:5000/docs](http://localhost:5000/docs).

Here is an example of payload for the `/prompt` endpoint, remember to update it according to your need:

- Update the model file name in the node **Load Checkpoint**
- Update the prompt in the node **CLIP Text Encode (Prompt)**

```json
{
  "prompt": {
    "1": {
      "inputs": {
        "seed": 1,
        "steps": 20,
        "cfg": 8,
        "sampler_name": "dpmpp_sde",
        "scheduler": "normal",
        "denoise": 1,
        "model": [
          "2",
          0
        ],
        "positive": [
          "4",
          0
        ],
        "negative": [
          "5",
          0
        ],
        "latent_image": [
          "3",
          0
        ]
      },
      "class_type": "KSampler",
      "_meta": {
        "title": "KSampler"
      }
    },
    "2": {
      "inputs": {
        "ckpt_name": "juggernaut-xl-v10.0.safetensors"
      },
      "class_type": "CheckpointLoaderSimple",
      "_meta": {
        "title": "Load Checkpoint"
      }
    },
    "3": {
      "inputs": {
        "width": 1024,
        "height": 1024,
        "batch_size": 1
      },
      "class_type": "EmptyLatentImage",
      "_meta": {
        "title": "Empty Latent Image"
      }
    },
    "4": {
      "inputs": {
        "text": "an astronaut riding a horse",
        "clip": [
          "2",
          1
        ]
      },
      "class_type": "CLIPTextEncode",
      "_meta": {
        "title": "CLIP Text Encode (Prompt)"
      }
    },
    "5": {
      "inputs": {
        "text": "",
        "clip": [
          "2",
          1
        ]
      },
      "class_type": "CLIPTextEncode",
      "_meta": {
        "title": "CLIP Text Encode (Negative Prompt)"
      }
    },
    "6": {
      "inputs": {
        "samples": [
          "1",
          0
        ],
        "vae": [
          "2",
          2
        ]
      },
      "class_type": "VAEDecode",
      "_meta": {
        "title": "VAE Decode"
      }
    },
    "save_image_websocket_node": {
      "inputs": {
        "images": [
          "6",
          0
        ]
      },
      "class_type": "SaveImageWebsocket",
      "_meta": {
        "title": "SaveImageWebsocket"
      }
    }
  }
}
```