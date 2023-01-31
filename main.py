from config          import *
from routers.account import account_router

app.include_router(account_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host  = '0.0.0.0',
        port  = 4080,
        debug = True
    )
