from sqlalchemy.exc import SQLAlchemyError

from src.core.exceptions import DatabaseException
from src.repositories.admin_repository import AdminRepository


class AdminService:
    def __init__(self, repository: AdminRepository):
        self.repository = repository

    def get_admin_dashboard_data(self):
        try:
            return {
                "total_users": self.repository.get_total_users(),
                "total_courses": self.repository.get_total_courses(),
                "total_results": self.repository.get_total_results(),
                "users": [
                    user.model_dump()
                    for user in self.repository.get_users_statistics()
                ],
                "recent_results": [
                    result.model_dump()
                    for result in self.repository.get_recent_results()
                ],
            }
        except SQLAlchemyError as exc:
            raise DatabaseException("Не вдалося завантажити дані адмін-панелі") from exc