from pydantic import BaseModel, ConfigDict


class CourseRead(BaseModel):
    id: int
    slug: str
    title: str

    model_config = ConfigDict(from_attributes=True)