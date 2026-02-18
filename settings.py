import os
from dotenv import load_dotenv

def get_default_env_path() -> str:
    return os.path.join(os.path.dirname(__file__), '.env')

def build_settings():
    # כאן תוכל להוסיף לוגיקה להורדת הגדרות מהסביבה או להגדיר ברירות מחדל
    load_dotenv()  # טוען את הגדרות ה־.env אם יש
    return {
        "some_setting": os.getenv("SOME_SETTING", "default_value"),
        "another_setting": os.getenv("ANOTHER_SETTING", "default_value"),
    }
