"""
This Python file defines a wrapper for the ClickUp API. 

Not all endpoints are implemented, but the most important ones are.

The API is documented here: https://clickup.com/api
"""


from datetime import datetime

import requests


class ClickUp:
    WEBHOOK_EVENTS = [
        "taskCreated",
        "taskUpdated",
        "taskDeleted",
        "taskPriorityUpdated",
        "taskStatusUpdated",
        "taskAssigneeUpdated",
        "taskDueDateUpdated",
        "taskTagUpdated",
        "taskMoved",
        "taskCommentPosted",
        "taskCommentUpdated",
        "taskTimeEstimateUpdated",
        "taskTimeTrackedUpdated",
        "listCreated",
        "listUpdated",
        "listDeleted",
        "folderCreated",
        "folderUpdated",
        "folderDeleted",
        "spaceCreated",
        "spaceUpdated",
        "spaceDeleted",
        "goalCreated",
        "goalUpdated",
        "goalDeleted",
        "keyResultCreated",
        "keyResultUpdated",
        "keyResultDeleted",
    ]

    def __init__(self, _api_key, _api_url=None) -> None:
        if _api_url:
            self.API_URL = _api_url
        else:
            self.API_URL = "https://api.clickup.com/api/v2"

        if not _api_key:
            raise Exception("Please provide api key to initialize api")
        elif len(_api_key) != 43:
            raise Exception("Provided api key is not correct")

        self.API_KEY = _api_key

    API_KEY = ""

    def create_folder(self, space_id: str, name: str) -> dict:
        resp = requests.post(
            url=f"{self.API_URL}/space/{str(space_id)}/folder",
            json={"name": name},
            headers={"Content-Type": "application/json", "Authorization": self.API_KEY},
        )

        data = resp.json()

        if resp.status_code != 200:
            raise ValueError(
                f"Server responded with error code {resp.status_code} {data}"
            )

        return data

    # folder/{folder_id}/list

    def create_list(self, folder_id: str, name: str) -> dict:
        resp = requests.post(
            url=f"{self.API_URL}/folder/{str(folder_id)}/list",
            json={"name": name},
            headers={"Content-Type": "application/json", "Authorization": self.API_KEY},
        )

        data = resp.json()

        if resp.status_code != 200:
            raise ValueError(
                f"Server responded with error code {resp.status_code} {data}"
            )

        return data

    def get_workspaces(self) -> dict:
        resp = requests.get(
            url=f"{self.API_URL}/team/", headers={"Authorization": self.API_KEY}
        )

        if resp.status_code != 200:
            raise ValueError(
                f"Server responded with error code {resp.status_code} {resp.json()}"
            )

        data = resp.json()

        return data

    # return workspace (in the url refered to as "team") attributes, else raise error

    def get_workspace_by_name(self, name: str) -> dict:
        resp = requests.get(
            url=f"{self.API_URL}/team/", headers={"Authorization": self.API_KEY}
        )

        if resp.status_code != 200:
            raise ValueError(
                f"Server responded with error code {resp.status_code} {resp.json()}"
            )

        data = resp.json()

        for team in data["teams"]:
            if team["name"] == name:
                return team

        raise NameError(f"Workspace with name {name} was not found")

    # return info of every member if a workspace
    def get_all_workspace_members(self, workspace_name: str) -> dict:
        workspace = self.get_workspace_by_name(name=workspace_name)
        return workspace["members"]

    def get_workspace_spaces(self, workspace_id: int) -> dict:
        resp = requests.get(
            url=f"{self.API_URL}/team/{str(workspace_id)}/space",
            data={"archived": "false"},
            headers={"Authorization": self.API_KEY},
        )

        data = resp.json()

        if resp.status_code != 200:
            raise ValueError(
                f"Server responded with error code {resp.status_code} {data}"
            )

        return data["spaces"]

    def get_space_by_name(self, workspace_id: int, name: str) -> dict:
        spaces = self.get_workspace_spaces(workspace_id=workspace_id)

        for space in spaces:
            if space["name"] == name:
                return space

        raise NameError(
            f"No space with name {name} was located in workspace with id {workspace_id}"
        )

    def get_workspace_id_by_name(self, name: str) -> int:
        return self.get_workspace_by_name(name)["id"]

    def get_space_folders(self, space_id: int) -> list:
        resp = requests.get(
            url=f"{self.API_URL}/space/{str(space_id)}/folder",
            data={"archived": "false"},
            headers={"Authorization": self.API_KEY},
        )

        data = resp.json()

        if resp.status_code != 200:
            raise ValueError(
                f"Server responded with error code {resp.status_code} {data}"
            )

        return data["folders"]

    def get_space_folder_by_name(self, space_id: int, name: str) -> dict:
        folders = self.get_space_folders(space_id)

        for folder in folders:
            if folder["name"] == name:
                return folder

        raise NameError(
            f"No folder with name {name} was found in space with id {space_id}"
        )

    def get_folder_lists(self, folder_id: int) -> list:
        resp = requests.get(
            url=f"{self.API_URL}/folder/{str(folder_id)}/list",
            data={"archived": "false"},
            headers={"Authorization": self.API_KEY},
        )

        data = resp.json()

        if resp.status_code != 200:
            raise ValueError(
                f"Server responded with error code {resp.status_code} {data}"
            )

        return data["lists"]

    def get_folder_list_by_name(self, folder_id: int, name: str) -> dict:
        lists = self.get_folder_lists(folder_id)

        for list in lists:
            if list["name"] == name:
                return list

        raise NameError(
            f"No list with name {name} was found in a folder with id {folder_id}"
        )

    def create_webhook(
        self,
        workspace_id: int,
        endpoint: str,
        events: list[str],
        space_id: int = None,
        folder_id: int = None,
        list_id: int = None,
        task_id: str = None,
    ):
        if not space_id and not folder_id and not list_id and not task_id:
            raise ValueError("No id was provided for object that webhook listens to")

        for event in events:
            if not event in self.WEBHOOK_EVENTS:
                raise ValueError(f"Provided event {event} is not valid webhook event")

        req_data = {"endpoint": endpoint, "events": events}

        if space_id:
            req_data["space_id"] = space_id

        if folder_id:
            req_data["folder_id"] = folder_id

        if list_id:
            req_data["list_id"] = list_id

        if task_id:
            req_data["task_id"] = task_id

        resp = requests.post(
            url=f"{self.API_URL}/team/{workspace_id}/webhook",
            json=req_data,
            headers={"Content-Type": "application/json", "Authorization": self.API_KEY},
        )
        if resp.status_code != 200:
            raise ValueError(
                f"Server responded with error code {resp.status_code} {resp.content}"
            )

        data = resp.json()

        return data

    def get_webhooks(self, workspace_id: str):
        resp = requests.get(
            url=f"{self.API_URL}/team/{workspace_id}/webhook",
            headers={"Content-Type": "application/json", "Authorization": self.API_KEY},
        )
        if resp.status_code != 200:
            raise ValueError(
                f"Server responded with error code {resp.status_code} {resp.content}"
            )

        data = resp.json()

        return data

    def get_task_by_id(self, task_id: str):
        resp = requests.get(
            url=f"{self.API_URL}/task/{task_id}",
            headers={"Content-Type": "application/json", "Authorization": self.API_KEY},
        )
        if resp.status_code != 200:
            raise ValueError(
                f"Server responded with error code {resp.status_code} {resp.content}"
            )

        data = resp.json()

        return data

    def delete_webhook_by_id(self, webhook_id: str):
        resp = requests.delete(
            url=f"{self.API_URL}/webhook/{webhook_id}",
            headers={"Content-Type": "application/json", "Authorization": self.API_KEY},
        )
        if resp.status_code != 200:
            raise ValueError(
                f"Server responded with error code {resp.status_code} {resp.content}"
            )

        data = resp.json()

        return data

    def add_comment_to_task(
        self, task_id: str, comment: str, notify_all: bool = False, assignee: int = None
    ):
        # https://api.clickup.com/api/v2/task/{task_id}/comment
        payload = {"comment_text": comment, "notify_all": notify_all}
        if assignee != None:
            payload["assignee"] = assignee

        resp = requests.post(
            url=f"{self.API_URL}/task/{str(task_id)}/comment",
            headers={"Content-Type": "application/json", "Authorization": self.API_KEY},
            json=payload,
        )

        if resp.status_code != 200:
            raise ValueError(
                f"Server responded with error code {resp.status_code} {resp.content}"
            )

        # data = resp.json()

        return True

    # missing implementation for getting the custom field id, otherwise works
    def set_custom_field_value(self, task_id: str, field_id: str, value):
        # https://api.clickup.com/api/v2/task/{task_id}/field/{field_id}

        #
        req = requests.post(
            self.API_URL + "/task/" + task_id + "/field/" + field_id,
            headers={"Authorization": self.API_KEY, "Content-Type": "application/json"},
            json={"value": value},
        )

        if req.status_code != 200:
            raise ValueError(
                f"Server responded with error code {req.status_code} {req.content}"
            )

        return True

    # type: ignore
    def create_task(
        self,
        list_id: int,
        name: str,
        description: str = None,
        assignees: list[int] = None,
        status: str = None,
        priority: int = None,
        due_date: datetime = None,
        parent: str = None,
        tags: list[str] = None,
    ) -> dict:
        req_data = {"name": name}

        if description != None:
            req_data["description"] = description

        # assignees
        if assignees != None:
            req_data["assignees"] = assignees  # type: ignore

        if status != None:
            req_data["status"] = status

        if priority != None:
            req_data["priority"] = priority  # type: ignore

        # duedate must be provided in milliseconds
        if due_date != None:
            if type(due_date) == datetime:
                req_data["due_date"] = int(due_date.timestamp() * 1000)  # type: ignore
            elif type(due_date) == int:
                req_data["due_date"] = due_date  # type: ignore

        if parent != None:
            req_data["parent"] = parent

        if tags != None:
            req_data["tags"] = tags  # type: ignore

        # notify all assignees and watchers of the task
        req_data["notify_all"] = False

        resp = requests.post(
            url=f"{self.API_URL}/list/{str(list_id)}/task",
            json=req_data,
            headers={"Content-Type": "application/json", "Authorization": self.API_KEY},
        )

        if resp.status_code != 200:
            raise ValueError(
                f"Server responded with error code {resp.status_code} {resp.content}"
            )

        data = resp.json()
        return data
