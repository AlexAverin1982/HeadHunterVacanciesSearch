class Vacancy:
    def __init__(self, fields: dict):
        if isinstance(fields, dict):
            self.id: str = fields.get('id', '')
            self.name: str = fields.get('name', '')
            self.has_test: bool = fields.get('has_test', False)

            area = fields.get('area', {})
            self.area: str = area.get('name', '')
            self.salary = fields.get('salary')
            self.publish_date: str = fields.get('published_at')
            snippet = fields.get('snippet', {})
            self.description = snippet.get('requirement')
            self.duty = snippet.get('responsibility')
            schedule = fields.get('schedule', {})
            self.job_type = schedule.get('name', '')

