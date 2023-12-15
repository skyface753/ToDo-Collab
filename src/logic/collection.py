import src.api.v1.endpoints.member.crud as member_crud
import src.api.v1.endpoints.collection.crud as collection_crud


async def find_collections_for_user(user_id: str):
    members = await member_crud.find_by_user_id(user_id)
    if members is None:
        return []
    collections = []
    for member in members:
        collection = await collection_crud.find_by_id(member.collection_id)
        if collection is not None:
            collections.append(collection)
    return collections
