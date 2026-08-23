from fastapi import FastAPI, HTTPException


app = FastAPI()



@app.get("/")
async def root():
    return {
            "name": "Task API",
            "version": "1.0"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

