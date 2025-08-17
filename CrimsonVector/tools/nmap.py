from utils import run_command, log_output

class NmapTool:
    def __init__(self, target: str):
        self.target = target
        
    async def scan(self, stdout_cb, stderr_cb):
        cmd = f"nmap {self.target}"
        await run_command(cmd, stdout_cb, stderr_cb)
        log_output("nmap", f"Scanned {self.target}\n")