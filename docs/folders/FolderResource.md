## Folder Resource
This class has different functionalities for the same endpoint, depending on the type of request made to the server. In this case it accepts "GET", "PUT", "DELETE".

**URL**: localhost:[PORT]/folders/api/v1/<folder_id>

**Methods**: `GET`, `PUT`, `DELETE`

**Authentication**: Required

## `GET` Method
**Code**: `200 OK`

**Content**:
```bash
{
    "data": {
        "folder": {
            "id": "Id from the folder",
            "name_folder": "Name for the folder",
            "user_id": "Id from the user"
        },
        "tasks": [
            {
                "name": "Name of the task",
                "body":  "Body of the task",
                "status": "Status of the task",
                "folder_id": "Id from the folder"
            },
            ...
        ],
        "events": [
            {
                "name_event": "Name for the event",
                "folder_id": "Id from the folder",
                "localization": "Localization from the event",
                "start_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00",
                "end_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00"
            },
            ...
        ]
    }
}
```

---

## `PUT` Method

**Required fields:** `name_folder`

```bash
{
    "name_folder": "New name for the folder"
}
```

### Success response
**Code**: `200 OK`
```bash
{
    "status": "Updated",
    "folder": {
        "id": "Id from the folder",
        "name_folder": "Name for the folder",
        "user_id": "Id from the user"
    }
}
```

## `DELETE` Method

### Success response
**Code**: `200 OK`
```bash
{
    "status": "Deleted"
}
```

## Error response
**Condition**: If the user wants to enter another user's folders.

**Code**: `403 FORBIDDEN`

**Content**:
```bash
{
    "error": "Unauthorized access to this folder"
}
```

