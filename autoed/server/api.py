from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from autoed.autoed import AutoedDaemon, kill_process_and_children
from autoed.server.auth import validate_token

autoed_daemon = AutoedDaemon()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/api/v1", dependencies=[Depends(validate_token)])


class Watcher(BaseModel):
    path: str
    pid: int


@router.get("/watchers")
async def get_watchers() -> list[Watcher]:
    return [
        {"path": d, "pid": autoed_daemon.pids[d]} for d in autoed_daemon.directories
    ]


class PID(BaseModel):
    pid: int


@router.get("/watchers/{path:path}/pid")
async def get_watcher_pid(path: str) -> PID:
    return autoed_daemon.pids[path]


class WatcherSetup(BaseModel):
    path: str
    inotify: bool = False
    sleep_time: float = 30
    log_dir: str = ""
    slurm: bool = False


@router.post("/watcher")
async def start_watcher(watcher_setup: WatcherSetup):
    autoed_daemon.watch(
        dirname=watcher_setup.path,
        use_inotify=watcher_setup.inotify,
        sleep_time=watcher_setup.sleep_time,
        log_dir=watcher_setup.log_dir,
        no_slurm=not watcher_setup.slurm,
    )


@router.delete("/watchers/{pid}")
async def stop_watcher(pid: int):
    if pid in autoed_daemon.pids.values():
        kill_process_and_children(pid)