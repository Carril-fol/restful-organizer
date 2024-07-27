## Folder Resource
This class has different functionalities for the same endpoint, depending on the type of request made to the server. In this case it accepts "GET", "PUT", "DELETE".

**URL**: localhost:[PORT]/tasks/api/v1/<task_id>

**Methods**: `GET`, `PUT`, `DELETE`

**Authentication**: Required

## `GET` Method
**Code**: `200 OK`

### Application data:
**Content**:
```bash
{
    "task": {
        "name": "Name of the task",
        "body":  "Body of the task",
        "status": "Status of the task",
        "folder_id": "Id from the folder"
    }
}

```

## `PUT` Method

### Application data:
**Content**:
```bash
{
    "name": "Name of the task",
    "body":  "Body of the task",
    "status": "Status of the task",
    "folder_id": "Id from the folder"
}
```

### Success response
**Code**: `200 OK`
```bash
{
    "status": "Updated",
    "task": {
        "id": "Id from the task",
        "name": "Name of the task",
        "body":  "Body of the task",
        "status": "Status of the task",
        "folder_id": "Id from the folder"
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

## Errors response

**Condition**: If the user who makes the request is not the creator of the tasks.

**Code**: `403 FORBIDDEN`

**Content**:
```bash
{
    "error": "Unauthorized access to this task"
}
```

----

**Condition**: If the task not exists.

**Code**: `404 NOT FOUND`

**Content**:
```bash
{
    "error": "Task not found."
}
```
