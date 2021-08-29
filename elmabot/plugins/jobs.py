import time
import asyncio
import yaml
import re

from croniter import croniter

from elmabot import elmabot, settings
from elmabot.modules import dbhelper as db
from elmabot.modules.utils import is_mongo_alive, get_jobs_as_string


SLEEP_TIME = 10
JOB_DAEMON_STATUS = True
ADD_JOB_PATTERN = re.compile(r"^.job add([\s\S]*)", re.MULTILINE)
ADD_JOB_WARNING = (
    'Please use YAML format as below:\n\n'
    '```.job add\n\n'
    'name: name\n'
    'source: -111\n'
    'target: -222\n'
    'parser: quiz\n'
    # 'interval: 33\n'
    'crontab: "0 * * * *"\n'
    'limit: 5\n'
    'last_value: 2392232\n'
    'extra:\n'
    '  example_extra: with_value```\n\n'
    '**PARAMETERS:**\n\n'
    '**name:** job name\n'
    '**source:** the source channel ID to get content from\n'
    '**target:** the target channel ID to post in\n'
    '**parser:** the parser to be used (quiz, pdf)\n'
    # '**interval:** kaç saniyede bir çalışacağı\n'
    '**crontab:** date and time in cron schedule exp format to run job\n'
    '**limit:** number of posts to be processed in each run \n'
    '**last_value:** the post to start from. use - to leave empty. '
    'use the .messageid command to get the message ID, or if you are not the '
    'admin you can copy the link and copy the message ID placed after the /\n'
    '**extra:** if your parser uses extra values, you can specify them in '
    'this block.'
    )


@elmabot.handle(outgoing=True, pattern=r"^.job daemon (start|stop|toggle)$")
async def toggle_job_daemon(event):
    global JOB_DAEMON_STATUS
    action = event.pattern_match.group(1)

    if action == 'toggle':
        JOB_DAEMON_STATUS ^= True  # toggle boolean
    elif action == 'start':
        JOB_DAEMON_STATUS = True
    else:
        JOB_DAEMON_STATUS = False

    await event.edit(f'`JOB_DAEMON_STATUS: {JOB_DAEMON_STATUS}`')


def should_run_job(job):
    cron = croniter(job['crontab'], time.time())
    return cron.get_prev() >= job['timestamp']


async def job_daemon():
    global JOB_DAEMON_STATUS
    global SLEEP_TIME
    await asyncio.sleep(SLEEP_TIME)  # add delay for connection to be done

    if not is_mongo_alive():
        return settings.LOGGER.error('Cannot connect to the MongoDB server.')

    while JOB_DAEMON_STATUS:
        jobs = await db.get_jobs(status=True)
        waiting_jobs = [j for j in jobs if should_run_job(j)]

        parser_list = {
            # 'pdf': pdf_parser,
            # 'quiz': quiz_parser,
            # 'text': text_parser,
            # 'english_word': english_word_parser,
        }
        for job in waiting_jobs:
            parser = parser_list[job['parser']]
            result = await parser(job)

            log = f"{job['_id']} - {job['name']} - finished"
            settings.LOGGER.info(log)

            if result.return_value:
                await db.update_job(
                    job['_id'], result.return_value, time.time())

        log = f'sleeping for {SLEEP_TIME} seconds before the next job...'
        settings.LOGGER.info(log)
        await asyncio.sleep(SLEEP_TIME)


elmabot.loop.create_task(job_daemon())


@elmabot.handle(outgoing=True, pattern=r"^.job list$")
async def list_jobs(event):
    if not is_mongo_alive():
        return await event.edit('`the MongoDB connection is not active.`')
    message = get_jobs_as_string(await db.get_jobs())
    await event.edit(message)


@elmabot.handle(outgoing=True, pattern=ADD_JOB_PATTERN)
async def add_job(event):
    if not event.pattern_match.group(1):
        return await event.edit(ADD_JOB_WARNING)

    try:
        input_arguments = event.pattern_match.group(1).strip()
        arguments = yaml.safe_load(input_arguments)

        if not croniter.is_valid(arguments['crontab']):
            return await event.reply('`crontab is not valid`')

        # TODO: use **kwargs
        add_job = await db.add_job(
            name=arguments['name'],
            source_chat=arguments['source'],
            target_chat=arguments['target'],
            parser=arguments['parser'],
            # interval=interval,
            crontab=arguments['crontab'],
            limit=arguments['limit'],
            last_value=arguments['last_value'],
            extra=arguments.get('extra'))
    except Exception as e:
        return await event.reply(
            '```an error occurred while processing the arguments:\n'
            f'{str(e)}```')

    job_list_str = get_jobs_as_string(await db.get_jobs())
    message = (
        '✅ `A new job was added.`\n\n'
        if add_job is True else
        '`Such a job already exists. ID: {}.`\n\n'.format(add_job["_id"]))
    await event.edit(message + job_list_str)


@elmabot.handle(outgoing=True, pattern=r"^.job (start|stop) (\w+)$")
async def toggle_job(event):
    action = event.pattern_match.group(1)
    job_id = event.pattern_match.group(2)
    job = await db.get_job(job_id=job_id)

    if not job:
        return await event.edit('`no such job.`')

    await db.update_job_status(job_id=job_id, status=action == 'start')
    message = get_jobs_as_string(await db.get_jobs())
    await event.edit('✅ **The job has been updated.** \n\n' + message)


@elmabot.handle(outgoing=True, pattern=r"^.job delete (\w+)$")
async def delete_job(event):
    job_id = event.pattern_match.group(1)
    job = await db.get_job(job_id=job_id)

    if not job:
        return await event.edit('`no such job.`')

    await db.delete_job(job_id=job_id)
    message = get_jobs_as_string(await db.get_jobs())
    await event.edit('✅ **The job has been deleted.** ' + message)
