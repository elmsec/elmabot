import time
from elmabot import settings
from bson.objectid import ObjectId


async def get_jobs(status=None):
    return settings.MONGO.jobs.find(
        {'status': status} if status is not None else {})


async def get_job(job_id):
    return settings.MONGO.jobs.find_one({'_id': ObjectId(job_id)})


async def delete_job(job_id):
    return settings.MONGO.jobs.delete_one({'_id': ObjectId(job_id)})


async def add_job(
        name, source_chat, target_chat, parser,
        crontab, limit=5, last_value=1, timestamp=None, extra={}):
    found_job = await get_job_by_info(source_chat, target_chat, parser)

    if found_job:
        return found_job

    settings.MONGO.jobs.insert_one(
        {
            'name': name,
            'source_chat': source_chat,
            'target_chat': target_chat,
            'parser': parser,
            'status': True,
            'crontab': crontab,
            'limit': limit,
            'last_value': int(last_value) if last_value else last_value,
            'timestamp': timestamp or time.time(),
            'extra': extra,
        }
    )

    return True


async def update_job(job_id, last_value, timestamp):
    return settings.MONGO.jobs.update_one(
        {'_id': ObjectId(job_id)},
        {'$set': {'last_value': last_value, 'timestamp': timestamp}})


async def update_job_status(job_id, status):
    return settings.MONGO.jobs.update_one(
        {'_id': ObjectId(job_id)}, {'$set': {'status': status}})


async def update_job_last_value(job_id, last_value):
    return settings.MONGO.jobs.update_one(
        {'_id': ObjectId(job_id)}, {'$set': {'last_value': last_value}})


async def update_job_timestamp(job_id, timestamp):
    return settings.MONGO.jobs.update_one(
        {'_id': ObjectId(job_id)}, {'$set': {'timestamp': timestamp}})


async def get_job_by_info(source_chat=None, target_chat=None, parser=None):
    # if source_chat and target_chat and parser:
    return settings.MONGO.jobs.find_one({
        'source_chat': source_chat,
        'target_chat': target_chat,
        'parser': parser,
    })

    # THESE MAY RETURN MULTIPLE VALUES SO WE WILL WORK ON THESE LATER
    # if source_chat and target_chat:
    #     return settings.MONGO.jobs.find_one(
    #         {'source_chat': source_chat, 'target_chat': target_chat})

    # if source_chat:
    #     return settings.MONGO.jobs.find_one({'source_chat': source_chat})

    # if target_chat:
    #     return settings.MONGO.jobs.find_one({'target_chat': target_chat})
