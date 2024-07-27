## Create tasks
Allows to the users create tasks.

**URL**: localhost:[PORT]/tasks/api/v1/<folder_id>

**Method**: `POST`

**Authentication**: Required

## Application data:
```bash
{
    "name": "Name of the task",
    "body":  "Body of the task",
    "status": "Status of the task"
}
```

## Success response
**Code**: `200 OK`

**Content**:
```bash
{
    "status": "Created",
    "task": {
        "name": "Name of the task",
        "body":  "Body of the task",
        "status": "Status of the task",
        "folder_id": "Id from the folder"
    }
}
```

## Error response
**Condition**: If the user wants to create a event in another user's folders.

**Code**: `403 FORBIDDEN`

**Content**:
```bash
{
    "error": "Unauthorized access to this folder"
}
```