import json
import os


class DatabaseManager:
    file_name = "database.json"

    @staticmethod
    def append_db(data):
        with open(DatabaseManager.file_name, "r") as file:
            json_data = json.load(file)

        json_data.append(data)

        jsonString = json.dumps(json_data)

        with open(DatabaseManager.file_name, "w") as file:
            file.write(jsonString)

    @staticmethod
    def load_db():
        if not os.path.exists(DatabaseManager.file_name):
            with open(DatabaseManager.file_name, "w") as file:
                file.write("[]")
        with open(DatabaseManager.file_name, "r") as file:
            loaded_data = json.load(file)

        return loaded_data

    @staticmethod
    def update_item(selected_item, new_values):
        original_username = selected_item[1]
        platform = selected_item[0]

        with open(DatabaseManager.file_name, "r") as file:
            string_json = file.read()
            passwords = json.loads(string_json)
            index = next(
                index
                for index, password in enumerate(passwords)
                if password["username"] == original_username
                and password["platform"] == platform
            )
            found_password = passwords[index]

        if found_password:
            updated_password = {**passwords[index], **new_values}
            json_serialize = json.dumps(
                updated_password,
                default=lambda o: o.decode("utf-8") if isinstance(o, bytes) else o,
            )
            passwords[index] = json.loads(json_serialize)
            with open(DatabaseManager.file_name, "w") as file:
                json.dump(passwords, file)

        else:
            raise ValueError("Password couldn't found!")

    @staticmethod
    def delete_item(selected_item):
        username = selected_item[1]
        platform = selected_item[0]
        with open(DatabaseManager.file_name, "r") as file:
            json_string = file.read()
            passwords = json.loads(json_string)
            index = next(
                index
                for index, password in enumerate(passwords)
                if password["username"] == username
                and password["platform"] == platform
            )
            found_password = passwords[index]
        
        if found_password:
            del passwords[index]
            with open(DatabaseManager.file_name , "w") as file:
                json.dump(passwords,file)
        else:
            raise ValueError("Password couldn't found!")

