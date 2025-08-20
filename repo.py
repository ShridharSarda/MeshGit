import os, hashlib, json, time
from objects import FileBlob, Commit

class Repo:
    BASE_DIR = ".meshgit"
    OBJECTS = os.path.join(BASE_DIR, "objects")
    INDEX = os.path.join(BASE_DIR, "index.json")
    HEAD = os.path.join(BASE_DIR, "HEAD")

    @staticmethod
    def init_repo():
        os.makedirs(Repo.OBJECTS, exist_ok=True)
        with open(Repo.INDEX, "w") as f:
            json.dump({}, f)
        if not os.path.exists(Repo.HEAD):
            with open(Repo.HEAD, "w") as f:
                f.write("")
        print("Initialized empty MeshGit repository.")

    @staticmethod
    def add_file(filename):
        if not os.path.exists(filename):
            print(f"File {filename} not found!")
            return
        with open(filename, "rb") as f:
            content = f.read()
        blob = FileBlob(content)
        blob.save(Repo.OBJECTS)
        with open(Repo.INDEX, "r+") as f:
            index = json.load(f)
            index[filename] = blob.hash
            f.seek(0)
            json.dump(index, f)
            f.truncate()
        print(f"Added {filename} to staging.")

    @staticmethod
    def commit(message):
        with open(Repo.INDEX) as f:
            index = json.load(f)

        if not index:
            print("Nothing to commit!")
            return

        parent = None
        if os.path.getsize(Repo.HEAD) > 0:
            with open(Repo.HEAD) as f:
                parent = f.read().strip() or None

        commit = Commit(message, index, parent)
        commit.save(Repo.OBJECTS)

        with open(Repo.HEAD, "w") as f:
            f.write(commit.hash)

        with open(Repo.INDEX, "w") as f:
            json.dump({}, f)

        print(f"[{commit.hash[:7]}] {message}")

    @staticmethod
    def show_log():
        if os.path.getsize(Repo.HEAD) == 0:
            print("No commits yet.")
            return

        with open(Repo.HEAD) as f:
            curr = f.read().strip()

        while curr:
            commit = Commit.load(Repo.OBJECTS, curr)
            print(f"commit {commit.hash}")
            print(f"Date: {time.ctime(commit.timestamp)}")
            print(f"    {commit.message}\n")
            curr = commit.parent
