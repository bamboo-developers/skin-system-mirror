import uvicorn
from app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("run:app", host="127.0.0.1", port=5000, workers=4)
    #app.run(host="127.0.0.1", port=5000)
    # serve(app, host="127.0.0.1", port=5000) 