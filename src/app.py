from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from src.endpoints.todo.router import router as todo_router
from src.api.v1.endpoints.todo.router import router as todo_router_api
from uvicorn.config import LOGGING_CONFIG
IS_DEV = True
import uvicorn
app = FastAPI()

app.mount("/static", StaticFiles(directory="src/presentation/static"), name="static")



@app.get("/")
async def get():
    # Redirect to the todo page
    return RedirectResponse(url="/todo")

# Chat
app.include_router(todo_router, prefix="/todo", tags=["todo"])
app.include_router(todo_router_api, prefix="/api/v1/todo", tags=["todo/api/v1"])







def run():
    """ Run the application """
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = (
        "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    )
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = (
        '%(asctime)s [%(name)s] %(levelprefix)s %(client_addr)s - '
        '"%(request_line)s" %(status_code)s'
    )
    host = "127.0.0.1" if IS_DEV else "0.0.0.0"
    uvicorn.run(
        "src.app:app",
        host=host,
        port=8000,
        reload=bool(IS_DEV),
        log_config=LOGGING_CONFIG,
    )