import asyncio
import subprocess

async def main():
    subprocess.run(['watchfiles',"--filter", "python", 'python -u src/main.py'])

asyncio.run(main())