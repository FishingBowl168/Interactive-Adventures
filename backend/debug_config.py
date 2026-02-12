import sys
import os
sys.path.append(os.getcwd())

try:
    from Core.config import settings
    print("Settings loaded successfully!")
    print(settings.model_dump())
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"ERROR LOADING SETTINGS: {e}")
