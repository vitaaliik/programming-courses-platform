from src.repositories.admin_repository_sqlalchemy import AdminRepository


class AdminService:
    def __init__(self, repository: AdminRepository):
        self.repository = repository

    def get_admin_dashboard_data(self):
        return {
            "total_users": self.repository.get_total_users(),
            "total_courses": self.repository.get_total_courses(),
            "total_results": self.repository.get_total_results(),
            "users": self.repository.get_users_statistics(),
            "recent_results": self.repository.get_recent_results(),
        }