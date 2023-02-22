from fastapi import FastAPI

app = FastAPI()
app.version = "0.0.2"
app.title = "Finance API"

@app.get('/')
def message():
    return "Hello Financee API"