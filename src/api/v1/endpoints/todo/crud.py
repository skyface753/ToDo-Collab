from src.models.models import TodoModel, UserModel, TeamModel, UserTeamModel
from src.config.env import student_collection, team_collection, user_collection

async def create_todo(student: TodoModel) -> TodoModel:
    """
    Insert a new todo record.

    A unique `id` will be created and provided in the response.
    """
    new_todo = await student_collection.insert_one(
        student.model_dump(by_alias=True, exclude=["id"])
    )
    # Add the user name and team name to the response
    created_todo = await student_collection.find_one({"_id": new_todo.inserted_id})
    # Create user if not exists
    user = await user_collection.find_one({"_id": created_todo["user_id"]})
    if user is None:
        user = UserModel(name="UsernamePH", email="test", password="test")
        user = await user_collection.insert_one(
            user.model_dump(by_alias=True, exclude=["id"])
        )
        user = await user_collection.find_one({"_id": user.inserted_id})
    # Create team if not exists
    team = await team_collection.find_one({"_id": created_todo["team_id"]})
    if team is None:
        team = TeamModel(name="TeamNamePH", description="test")
        team = await team_collection.insert_one(
            team.model_dump(by_alias=True, exclude=["id"])
        )
        team = await team_collection.find_one({"_id": team.inserted_id})
    # Add the user name and team name to the response
    
    created_todo["user_name"] = user["name"]
    created_todo["team_name"] = team["name"]
    
    return created_todo