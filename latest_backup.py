import os

def get_latest_backup():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    os.makedirs("backups/backups", exist_ok=True)

    directory = os.path.join(project_root, "backups", "backups")
    files = os.listdir(directory)

    backups = [f for f in files if f[:4].isdigit() and "_" in f]

    if not backups:
        return None

    latest = max(backups)
    return os.path.join(directory, latest, "api.json")

if __name__ == "__main__":
    latest_backup = get_latest_backup()
    if latest_backup:
        print(f"Latest backup: {latest_backup}")
    else:
        print("No backups found")