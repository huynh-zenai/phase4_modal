# phase4_modal
# Deploy & Run Txt2Img SD-1.5 on Modal

## 1. Prerequisites

| Component                 | Notes                                                                 |
|--------------------------|-----------------------------------------------------------------------|
| **Python ≥ 3.10**        | Needed locally for the Modal CLI                                      |
| **Modal CLI**            | Install with: `pip install modal`                                     |
| **Modal account**        | Sign up, then run `modal setup` to create config & API token          |
| **Hugging Face token**   | Required for model download; store as secret `huggingface-secret`     |
| **Git (optional)**       | For cloning repositories and version control                          |

💡 *No local GPU required — everything runs on Modal’s cloud GPUs.*

## 2. Environment setup

#### 1. Clone the repo
```bash
git clone https://github.com/<your-org>/txt2img-modal.git
cd txt2img-modal
```
#### 2. Install the Modal CLI 
```bash
pip install --upgrade pip modal
```
#### 3. Login to Modal
```bash
modal setup
```
#### 4. Add your HD token as a secret
```bash
modal secret create huggingface-secret HF_TOKEN=hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

## 3. Quick local test (no deploy)
```bash
modal run app.py --prompt "Cyberpunk cat, neon skyline" --steps 30
```

## 4. Deploy the API
```bash
modal deploy app.py
```
The CLI prints a URL like:
```
https://txt2img-sd15--inference-web.modal.run
```

Below are two ways to test this endpoint.

## 4.1 cURL example
```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"prompt":"a red panda in a spacesuit"}' \
     https://txt2img-sd15--inference-web.modal.run/ \
| jq -r .data | base64 -d > panda.png
```

## 4.2 Python client snippet
```python3
python3 client.py
```
