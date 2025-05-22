from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Bot is running!"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=10000, reload=False)
