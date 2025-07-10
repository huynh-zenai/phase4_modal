import io, os, random, time, base64, modal
from pathlib import Path

APP_NAME = "txt2img-sd15"
app = modal.App(APP_NAME)

# 1) Build container image
image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "torch~=2.5",          
        "diffusers==0.31.0",  
        "transformers~=4.44",
        "accelerate~=0.33",
        "safetensors",
        "huggingface-hub[hf_transfer]~=0.25",
    )
    .env({
        "HF_HUB_ENABLE_HF_TRANSFER": "1",   #
    })
)

CACHE_DIR = "/cache"                      # volume cache model
cache_vol = modal.Volume.from_name("hf-cache", create_if_missing=True)

# 2) Inference class
@app.cls(
    image=image,
    gpu="T4",            
    timeout=600,
    volumes={CACHE_DIR: cache_vol},
    secrets=[modal.Secret.from_name("huggingface-secret")],
)
class Inference:
    @modal.enter()
    def load(self):
        from diffusers import StableDiffusionPipeline
        import torch
        model_id = "runwayml/stable-diffusion-v1-5"
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16
        ).to("cuda")

    @modal.method()
    def run(self, prompt: str, steps: int = 25, guidance: float = 7.5) -> bytes:
        images = self.pipe(prompt, num_inference_steps=steps, guidance_scale=guidance).images
        buf = io.BytesIO()
        images[0].save(buf, format="PNG")
        return buf.getvalue()

# 3) CLI entrypoint (local dev)
@app.local_entrypoint()
def main(prompt: str = "A serene lake at sunset"):
    t0 = time.time()
    img_bytes = Inference().run.remote(prompt)
    Path("output.png").write_bytes(img_bytes)
    print(f"Saved output.png – {time.time()-t0:.2f}s")