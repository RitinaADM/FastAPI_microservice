from contextlib import asynccontextmanager
from fastapi import FastAPI
from infrastructure.di.providers import get_container
from dishka.integrations.fastapi import setup_dishka


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    
    # Close container on app termination
    if hasattr(app.state, 'dishka_container'):
        await app.state.dishka_container.close()


def create_app() -> FastAPI:
    # Create DI container
    container = get_container()
    
    app = FastAPI(title="Category Service", version="1.0.0", lifespan=lifespan)
    
    # Setup Dishka integration
    setup_dishka(container=container, app=app)
    
    # Include routers
    from infrastructure.adapters.inbound.rest.category_controller import router as category_router
    app.include_router(category_router)
    
    @app.get("/")
    async def root():
        return {"message": "Category Service is running"}
    
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)