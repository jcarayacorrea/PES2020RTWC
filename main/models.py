from typing import Dict, Any, List, Optional

class Team:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.id = data.get('_id')
        self.code = data.get('code')
        self.nation_name = data.get('nation_name')
        self.image_flag = data.get('image_flag')
        self.fifa_nation_rank = data.get('fifa_nation_rank')
        self.conf_name = data.get('conf_name')
        self.progress = data.get('progress', {})

    def __getitem__(self, item):
        return self.data.get(item)

    def get(self, item, default=None):
        return self.data.get(item, default)


class Fixture:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.conf = data.get('conf')
        self.zone = data.get('zone')
        self.round = data.get('round')
        self.teams = [Team(t) for t in data.get('teams', [])]
        self.fixtures = data.get('fixtures', {})

    def __getitem__(self, item):
        return self.data.get(item)
