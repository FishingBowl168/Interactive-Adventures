import sys
import os
sys.path.append(os.getcwd())

try:
    print("Importing fastapi...")
    from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
    print("FastAPI imported.")
    
    print("Importing Core.config...")
    from Core.config import settings
    print("Config imported.")

    print("Importing db.database...")
    from db.database import get_db, SessionLocal
    print("DB imported.")

    print("Importing models...")
    from models.story import Story, StoryNode
    from models.job import StoryJob
    print("Models imported.")

    print("Importing schemas...")
    from schemas.story import CreateStoryRequest
    from schemas.job import StoryJobResponse
    print("Schemas imported.")
    
    print("Importing routers.story...")
    from routers import story
    print("Routers imported.")
    
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"IMPORT ERROR: {e}")
