from pydantic import BaseModel, UUID4, field_validator
from datetime import date
from typing import Optional


class TaskCreate(BaseModel):
    projectId: UUID4
    title: str
    status: str = "Backlog"
    assignee: Optional[str] = None
    dueDate: Optional[date] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ("Backlog", "Doing","Dont"):
            raise ValueError("status must be Backlog|Doing|Done")
        return v
    
class Task(TaskCreate):
    id: UUID4