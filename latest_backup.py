import os

def get_latest_backup():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    os.makedirs("backups/backups", exist_ok=True)

    directory = os.path.join(project_root, "static", "backups")
    files = os.listdir(directory)

    backups = [f for f in files if f[:4].isdigit() and "_" in f]

    if not backups:
        return None

    latest = max(backups)
    return os.path.join(directory, latest, "api.json")

def get_latest_images():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    directory = os.path.join(project_root, "static", "backups")  # look in static/backups
    if not os.path.exists(directory):
        return None
    files = os.listdir(directory)

    backups = [f for f in files if f[:4].isdigit() and "_" in f]

    if not backups:
        return None

    latest = max(backups)
    return os.path.join(directory, latest, "images.json")

def get_all_backups():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    
    directory = os.path.join(project_root, "static", "backups")
    if not os.path.exists(directory):
        return []
    files = os.listdir(directory)
    
    backups = [f for f in files if f[:4].isdigit() and "_" in f]
    backups.sort(reverse=True)
    return backups

def get_backup_path(backup_folder):
   project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
   return os.path.join(project_root, "static", "backups", backup_folder, "api.json")

if __name__ == "__main__":
    latest_backup = get_latest_backup()
    if latest_backup:
        print(f"Latest backup: {latest_backup}")
    else:
        print("No backups found")