import io
import tempfile
import uuid

from config import get_settings

from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from patho_predictor import run

def create_application() -> FastAPI:
    application = FastAPI()
    application.add_middleware(
        CORSMiddleware,
        allow_origins="http://localhost:3000",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application

app = create_application()

@app.post("/upload_file")
async def upload_file(
    file: UploadFile = File(...),
    settings = Depends(get_settings)
    ):
    try:
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".fasta") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name
        result_df = run(settings.complete_genome_model_path, tmp_path)
        buffer = io.StringIO()
        result_df.to_csv(buffer, index=False)
        buffer.seek(0)

        return StreamingResponse(
            iter([buffer.read()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={str(uuid.uuid4().hex)}.csv"
            }
        )
    except:
        return JSONResponse(status_code=400, content={"error: failed to fetch file"})
    
@app.post("/upload_sequence/{sequence}")
async def upload_file(
    sequence: str,
    settings = Depends(get_settings)
    ):
    try:
        if not check_genome(sequence):
            return JSONResponse(status_code=400, content="error: invalid genome format")
        sequence_id = str(uuid.uuid4().hex)
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".fasta") as tmp:
            tmp.write(f">seq_{sequence_id}\n")
            tmp.write(sequence)
            tmp_path = tmp.name
        result_df = run(settings.complete_genome_model_path, tmp_path)
        buffer = io.StringIO()
        result_df.to_csv(buffer, index=False)
        buffer.seek(0)

        return StreamingResponse(
            iter([buffer.read()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={sequence_id}.csv"
            }
        )
    except:
        return JSONResponse(status_code=400, content={"error: failed to fetch file"})
    
def check_genome(genome):
    accectable = set("ATCG")
    validation = set(genome)
    return validation.issubset(accectable)