class ReportService:
    def __init__(self, report_dao):
        self.report_dao = report_dao

    def employee_activity_summary(self):
        return self.report_dao.employee_activity_summary()
