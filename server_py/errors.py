class ApiError(Exception):
    """Raised anywhere in the backend; rendered as {"detail": message} with the given status."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail
