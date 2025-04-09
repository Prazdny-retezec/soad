from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from database import engine

# stores for persisting jobs and runs
job_stores = {'default': SQLAlchemyJobStore(engine=engine)}

# scheduler for task planning and executing
scheduler = AsyncIOScheduler(jobstores=job_stores)


def get_scheduler():
    return scheduler
