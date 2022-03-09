
import aiofiles
import imageio

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import StreamingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/predict")
async def upload_file(in_file: UploadFile = File(...)):

    # save video https://stackoverflow.com/questions/63580229/how-to-save-uploadfile-in-fastapi
    out_file_path = "bbb.mp4"

    async with aiofiles.open(out_file_path, "wb") as out_file:
        while content := await in_file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk

    # generate gif https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
    generated_gif_path = "a.gif"

    images = ["a.png", "b.png", "c.png"]
    loaded_images = [imageio.imread(f) for f in images]
    imageio.mimsave(generated_gif_path, loaded_images)

    # stream response https://fastapi.tiangolo.com/advanced/custom-response/#using-streamingresponse-with-file-like-objects
    def iterfile():
        with open(generated_gif_path, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="image/gif")
