# app.py
import gradio as gr
from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32
).to("cpu")

def generate(prompt):
    image = pipe(prompt).images[0]
    return image

iface = gr.Interface(fn=generate, inputs="text", outputs="image", title="LootBot Image Generator")
iface.launch()
