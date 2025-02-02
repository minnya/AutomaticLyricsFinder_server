from fastapi.responses import JSONResponse

class UTF8JSONResponse(JSONResponse):
    def __init__(self, content, **kwargs):
        super().__init__(content=content, **kwargs)
        self.headers["Content-Type"] = "application/json; charset=utf-8"