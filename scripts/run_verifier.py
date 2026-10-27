#!/usr/bin/env python3
"""Шаги глубины верификатора: dry → smoke → sweep → full."""
import subprocess, sys, time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "results" / "verifier_log.csv"

STEPS = [
    ("dry",   ["python", "checks/check.py"]),
    ("smoke", ["python", "-m", "pytest",
               "checks/test_properties.py", "-q"]),
    ("sweep", ["python", "-m", "pytest", "checks", "-q"]),
    ("full",  ["python", "checks/check_graph.py"]),
]


def main():
    LOG.parent.mkdir(exist_ok=True)
    LOG.write_text("datetime,step,status,seconds,code\n", encoding="utf-8")
    for name, cmd in STEPS:
        print(f"=== {name} ===")
        t0 = time.time()
        r = subprocess.run(cmd, cwd=ROOT)
        dt = time.time() - t0
        status = "pass" if r.returncode == 0 else "fail"
        print(f"{name}: {status.upper()} ({dt:.2f} c), код {r.returncode}")
        with LOG.open("a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')},"
                    f"{name},{status},{dt:.2f},{r.returncode}\n")
        if r.returncode != 0:
            print(f"СТОП: шаг {name}")
            sys.exit(1)
    print("Все шаги пройдены.")


if __name__ == "__main__":
    main()
