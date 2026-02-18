from pydantic import BaseModel

class ErrorInfo(BaseModel):
    code: str
    message: str
    details: dict | None = None

class ToolResult(BaseModel):
    ok: bool
    data: dict | None = None
    error: ErrorInfo | None = None

    def model_dump(self):
        """
        פוקנציה הממירה את המודל לפלט שניתן להחזיר אותו כ־JSON.
        """
        return self.dict(exclude_unset=True)
