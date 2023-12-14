from src.models.models import TodoModel, UserModel
from src.config.env import todo_collection, user_collection
from src.api.v1.endpoints.team.crud import find_by_id as find_team_by_id
from src.api.v1.endpoints.user.crud import find_by_id as find_user_by_id


async def create_todo(new_todo: TodoModel) -> TodoModel:
    """
    Insert a new todo record.

    A unique `id` will be created and provided in the response.
    """
    team = await find_team_by_id(new_todo["team_id"])
    if team is None:
        return None
    user = await find_user_by_id(new_todo["user_id"])
    if user is None:
        return None

    new_todo = await todo_collection.insert_one(
        new_todo.model_dump(by_alias=True, exclude=["id"])
    )
    # Add the user name and team name to the response
    created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})

    # Add the user name and team name to the response

    created_todo["user_name"] = user["name"]
    created_todo["team_name"] = team["name"]

    return created_todo
