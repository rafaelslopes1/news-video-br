import json


class Database:
    def __init__(self) -> None:
        print("[Database] Initialization...")
        self.__content_file_path = './data/content.json'

    def save(self, content):
        print(f"[Database] Saving content on {self.__content_file_path}...")
        with open(self.__content_file_path, 'w') as file:
            content_string = json.dumps(content, ensure_ascii=False, default=self.__todict, indent=2)
            file.write(content_string)

    def load(self):
        with open(self.__content_file_path, 'r') as file:
            file_buffer = file.read()
            content_json = json.loads(file_buffer)
            return content_json


    def __todict(self, obj, classkey=None):
        if isinstance(obj, dict):
            data = {}
            for (k, v) in obj.items():
                data[k] = self.__todict(v, classkey)
            return data
        elif hasattr(obj, "_ast"):
            return self.__todict(obj._ast())
        elif hasattr(obj, "__iter__") and not isinstance(obj, str):
            return [self.__todict(v, classkey) for v in obj]
        elif hasattr(obj, "__dict__"):
            data = dict([(key, self.__todict(value, classkey)) 
                for key, value in obj.__dict__.items() 
                if not callable(value) and not key.startswith('_')])
            if classkey is not None and hasattr(obj, "__class__"):
                data[classkey] = obj.__class__.__name__
            return data
        else:
            return obj
