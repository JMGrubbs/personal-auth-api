from fastapi import FastAPI

# from routes.main import main

app = FastAPI()

should_continue = True


@app.get("/")
def home():
    return {"Hello": "world"}


# app.include_router(main, prefix="/", tags=["main"])
