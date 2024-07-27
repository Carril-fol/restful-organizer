## Get folders by user ID
Allows to see to the users they own folders.

**URL**: localhost:[PORT]/folders/api/v1/user/<user_id>

**Method**: `GET`

**Authentication**: Required

## Success response
**Code**: `200 OK`

**Content**:
```bash
{
    "folders": [
        {
            "id": "Id from the folder",
            "name_folder": "Name for the folder",
            "user_id": "Id from the user"
        },
        ...
    ]
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