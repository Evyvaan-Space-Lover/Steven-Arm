from config import HOST, PORT
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "web.server:app",host=HOST,port=PORT,reload=True
    )
