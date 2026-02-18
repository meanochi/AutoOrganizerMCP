# כאן אתה יכול להגדיר קודי שגיאה כלליים לשימוש במערכת
GENERIC_ERROR = "GENERIC_ERROR"
FILE_NOT_FOUND = "FILE_NOT_FOUND"
INVALID_INPUT = "INVALID_INPUT"

# דוגמה למבנה שגיאה
def create_error(code: str, message: str, details: dict | None = None):
    return {
        "code": code,
        "message": message,
        "details": details
    }
