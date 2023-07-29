from mixer.backend.sqlalchemy import mixer
from sqlmodel import select


def is_response_match_object_fields(response_data, obj, fields):
    for field in fields:
        response_field = response_data[field]
        obj_field = str(obj[field] if type(obj) is dict else getattr(obj, field))
        if response_field != obj_field:
            return False
    return True


async def get_model_objects_count(model, session):
    result = await session.execute(select(model))
    return len(result.all())


async def delete_first_object(query, session):
    objs = await session.execute(query)
    obj = objs.first()[0]
    await session.delete(obj)
    await session.commit()