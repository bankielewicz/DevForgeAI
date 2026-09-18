import runner_probe as probe


if __name__ == "__main__":
    probe.RUN_DIR = probe.ROOT / "simulated-run-current"
    probe.main()
