import subprocess
import time

import docker
from docker.models.containers import Container

container_id: str = "af58574d79d2"
client = docker.from_env()
container: Container = client.containers.get(container_id)


def get_container_top_info():
    p = subprocess.Popen(
        "docker stats --no-stream",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    res = container.exec_run(["top", "-b", "-n", "1"])
    top_cpu_percent = sum(
        [float(a.split()[8]) for a in res.output.decode("utf8").split("\n")[7:] if a]
    )
    p.wait(5)
    if p.poll() == 0:
        stats = p.communicate()[0].split("\n")
        stat: dict = {a.split()[0]: a.split() for a in stats if a}
        cur_stat = stat.get(container_id)
        stat_cpu_percent = float(cur_stat[2][:-1])
    else:
        print("failed")
        return
    # https://juejin.cn/s/docker%20stats%20api%20cpu%20percentage
    # stats = container.stats(stream=False)
    # cpu_percent = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage']
    print(top_cpu_percent, stat_cpu_percent)
    pass


if __name__ == "__main__":
    for _ in range(1000):
        get_container_top_info()
        time.sleep(1)
