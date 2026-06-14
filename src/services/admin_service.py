from sqlalchemy.exc import SQLAlchemyError

from src.core.exceptions import DatabaseException
from src.repositories.admin_repository import AdminRepository
from src.schemas.admin import AdminDashboardDTO


class AdminService:
    def __init__(self, repository: AdminRepository):
        self.repository = repository

    def get_admin_dashboard_data(
    self,
    email_search: str = "",
    course_filter: str = "",
) -> dict:
        
      try:
        return {
            "total_users": self.repository.get_total_users(),
            "total_courses": self.repository.get_total_courses(),
            "total_results": self.repository.get_total_results(),

            "users": self.repository.get_users_statistics(),

            "recent_results": self.repository.get_recent_results(
                email_search,
                course_filter,
            ),

            "courses_filter": self.repository.get_all_courses_for_filter(),
        }

      except SQLAlchemyError as exc:
        raise DatabaseException(
            "Failed to load admin dashboard data"
        ) from exc