from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from .generate import inpaint, outpaint
from PIL import Image
import io
import base64

app = FastAPI()


@app.post("/edit")
async def edit(
    image: UploadFile = File(...),
    mask: UploadFile = File(...),
    prompt: str = Form(...),
    mode: str = Form("inpaint"),
):
    """Endpoint for basic inpainting and outpainting."""
    img_bytes = await image.read()
    mask_bytes = await mask.read()
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    msk = Image.open(io.BytesIO(mask_bytes)).convert("L")
    if mode == "outpaint":
        result = outpaint(img, msk, prompt)
    else:
        result = inpaint(img, msk, prompt)
    buf = io.BytesIO()
    result.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return JSONResponse({"image": b64})
