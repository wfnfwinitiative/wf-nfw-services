from app.repositories.report_repository import ReportRepository


class ReportService:
    def __init__(self, db):
        self.repo = ReportRepository(db)

    async def get_report(self, filters):
        grid = await self.repo.get_report_data(filters)
        graph = await self.repo.get_graph_data(filters)
        summary = await self.repo.get_summary(filters)

        return {
            "summary": summary,
            "grid": grid,
            "graph": graph
        }