import asyncio
import datetime
import os

LOG_DIR = "logs"

def log_output(tool_name: str, output: str):
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{LOG_DIR}/{tool_name}_{timestamp}.log"
    with open(filename, "a") as f:
        f.write(output)

async def run_command(cmd: str, callback_stdout=None, callback_stderr=None):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    while True:
        line = await process.stdout.readline()
        if line:
            decoded = line.decode().strip()
            if callback_stdout:
                callback_stdout(decoded)
        else:
            break
    err = await process.stderr.read()
    if err and callback_stderr:
        callback_stderr(err.decode().strip())
    await process.wait()
