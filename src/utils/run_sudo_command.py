import subprocess
from typing import Optional, TypedDict


class CommandReturn(TypedDict):
    success: bool
    stdout: Optional[str]
    stderr: Optional[str]
    returncode: int


def run_sudo_command(command: str, password: str | None = None) -> CommandReturn:
    try:
        if password:
            process = subprocess.run(
                ["sudo", "-S"] + command.split(),
                input=f"{password}\n",
                text=True,
                capture_output=True,
                check=True,
            )
        else:
            process = subprocess.run(
                ["sudo"] + command.split(), capture_output=True, text=True, check=True
            )

        # Return output, error, and return code
        return {
            "success": True,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "returncode": process.returncode,
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "stdout": e.stdout,
            "stderr": e.stderr,
            "returncode": e.returncode,
        }
