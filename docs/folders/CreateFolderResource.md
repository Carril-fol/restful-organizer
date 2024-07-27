## Create folders.
Allows to the users create folders.

**URL**: localhost:[PORT]/events/api/v1/<folder_id>

**Method**: `POST`

**Authentication**: Required

## Application data:
```bash
{
    "name_folder": "Name for the folder",
    "user_id": "Id from the user"
}
```

## Success response
**Code**: ` 201 CREATED`

**Content**:
```bash
{
    "status": "Created",
    "folder": {
        "id": "Id from the folder",
        "name_folder": "Name for the folder",
        "user_id": "Id from the user"
    }
}
```

## Error response
**Condition**: If the user wants to create a folder with the token blacklisted.

**Code**: `400 BAD REQUEST`

**Content**:
```bash
{
    "error": "Token is already blacklisted"
}
```