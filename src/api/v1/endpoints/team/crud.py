from src.models.models import TeamModel
from src.config.env import team_collection


async def create_team(name: str, description: str) -> TeamModel:
    """ Create a new Team """
    team = TeamModel(name=name, description=description)
    team = await team_collection.insert_one(
        team.model_dump(by_alias=True, exclude=["id"])
    )
    team = await find_by_id(team.inserted_id)
    return team


async def find_by_name(name: str) -> TeamModel:
    """
    Find a team by its unique name.
    """
    team = await team_collection.find_one({"name": name})
    if team is None:
        return None
    return TeamModel(**team)


async def find_by_id(id: str) -> TeamModel:
    """
    Find a todo by its unique id.
    """
    team = await team_collection.find_one({"_id": id})
    if team is None:
        return None
    return TeamModel(**team)
