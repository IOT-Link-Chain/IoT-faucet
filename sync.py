from apscheduler.schedulers.blocking import BlockingScheduler
from service.sync import process_faucet

if __name__ == "__main__":
    scheduler = BlockingScheduler()

    scheduler.add_job(process_faucet, "interval", minutes=5)

    scheduler.start()
