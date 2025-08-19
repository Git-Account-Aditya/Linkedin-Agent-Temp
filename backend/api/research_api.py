from typing import Dict, Any, List


class researchapi:
    def __init__(self, api):
        self.api = api

    async def fetch_trends(self, field: str) -> List[Dict[str, Any]]:

        # Simulate fetching research trends


        # demo return
        return [
            {
                "title": "Trend 1",
                "summary": 'increasing in near future',
                "sources": {
                    "source_1": "https://source-a.com",
                    "source_2": "https://source-b.com"
                }
            },
            {
                "title": "Trend 2",
                "summary": 'decreasing in near future',
                "sources": {
                    "source_1": "https://source-c.com",
                    "source_2": "https://source-d.com"
                }
            }   
        ]