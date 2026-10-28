"""Tower of Hanoi: recursive state-space solution. Standard library only."""

def hanoi(n, source="A", auxiliary="B", target="C"):
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    hanoi(n - 1, source, target, auxiliary)
    print(f"Move disk {n} from {source} to {target}")
    hanoi(n - 1, auxiliary, source, target)

if __name__ == "__main__":
    raw = input("Number of disks [3]: ").strip()
    n = int(raw) if raw else 3
    if not 1 <= n <= 20:
        raise SystemExit("Choose between 1 and 20 disks to avoid enormous output.")
    hanoi(n)
    print(f"Minimum moves: {2**n - 1}")
