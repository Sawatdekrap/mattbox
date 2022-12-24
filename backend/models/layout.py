from typing import Dict

from pydantic import BaseModel

from models.component import Component


class Layout(BaseModel):
    game_id: str
    player_id: str
    components: Dict[str, Component] = {}

    def add_component(self, component: Component) -> None:
        assert component.id not in self.components
        self.components[component.id] = component
