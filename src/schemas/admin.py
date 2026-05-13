from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AdminUserStatisticsDTO(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime | None
    tests_passed: int
    avg_result: float
    completed_courses: int
    last_activity: datetime | None

    model_config = ConfigDict(from_attributes=True)


class RecentTestResultDTO(BaseModel):
    username: str
    email: str
    course_title: str
    score: int
    total: int
    passed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class AdminDashboardDTO(BaseModel):
    total_users: int
    total_courses: int
    total_results: int
    users: list[AdminUserStatisticsDTO]
    recent_results: list[RecentTestResultDTO]