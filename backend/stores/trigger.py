from collections import defaultdict
from typing import Dict, List

from models.update import UpdateType
from models.trigger import Trigger


TypeTriggers = Dict[UpdateType, List[Trigger]]
GAME_TRIGGERS: Dict[str, TypeTriggers] = defaultdict(lambda: defaultdict(list))


def add_trigger_to_game(game_id: str, trigger: Trigger) -> None:
    type_triggers = GAME_TRIGGERS[game_id]
    type_triggers[trigger.update_type].append(trigger)


def get_triggers_of_type(game_id: str, update_type: UpdateType) -> List[Trigger]:
    type_triggers = GAME_TRIGGERS[game_id]
    triggers = type_triggers[update_type]

    return triggers
