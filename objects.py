import os, hashlib, json, time

class FileBlob:
    def __init__(self, content):
        self.content = content
        self.hash = hashlib.sha1(content).hexdigest()

    def save(self, obj_dir):
        path = os.path.join(obj_dir, self.hash)
        if not os.path.exists(path):
            with open(path, "wb") as f:
                f.write(self.content)

class Commit:
    def __init__(self, message, files, parent=None):
        self.message = message
        self.files = files
        self.parent = parent
        self.timestamp = time.time()
        raw = f"{message}{files}{parent}{self.timestamp}".encode()
        self.hash = hashlib.sha1(raw).hexdigest()

    def save(self, obj_dir):
        path = os.path.join(obj_dir, self.hash + ".json")
        with open(path, "w") as f:
            json.dump(self.__dict__, f)

    @staticmethod
    def load(obj_dir, commit_hash):
        path = os.path.join(obj_dir, commit_hash + ".json")
        with open(path) as f:
            data = json.load(f)
        commit = Commit(data["message"], data["files"], data["parent"])
        commit.timestamp = data["timestamp"]
        commit.hash = data["hash"]
        return commit
