from pydantic import BaseModel, field_validator


class SuccessOperation(BaseModel):
    success: bool

    # success has to be true
    @field_validator("successs", check_fields=False)
    @classmethod
    def field_is_true(cls, v):
        if not v:
            raise ValueError("success must be True")
        return v
