## Event Resource
This class has different functionalities for the same endpoint, depending on the type of request made to the server. In this case it accepts "GET", "PUT", "DELETE".

**URL**: localhost:[PORT]/events/api/v1/<event_id>

**Methods**: `GET`, `PUT`, `DELETE`

**Authentication**: Required

## `GET` Method
**Code**: `200 OK`

**Content**:
```bash
{
    "event": {
        "name_event": "Name for the event",
        "folder_id": "Id from the folder",
        "localization": "Localization from the event",
        "start_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00",
        "end_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00"
    }
}
```

## `PUT` Method

### Application data:
```bash
{
    "name_event": "Name for the event",
    "folder_id": "Id from the folder",
    "localization": "Localization from the event",
    "start_date": "Date in the format: YYYY-MM-DD (e.g., 2024-07-20) or YYYY-MM-DDTHH:MM:SS (e.g., 2024-07-20T14:30:00). 
        For formats including milliseconds and timezone, use: YYYY-MM-DDTHH:MM:SS.MS+00:00 (e.g., 2024-07-20T14:30:00.123+00:00).",
    "end_date": "Date in the format: YYYY-MM-DD (e.g., 2024-07-20) or YYYY-MM-DDTHH:MM:SS (e.g., 2024-07-20T14:30:00). 
        For formats including milliseconds and timezone, use: YYYY-MM-DDTHH:MM:SS.MS+00:00 (e.g., 2024-07-20T14:30:00.123+00:00)."
}
```

### Success response
**Code**: `200 OK`
```bash
{
    "status": "Updated",
    "event": {
        "name_event": "Name for the event",
        "folder_id": "Id from the folder",
        "localization": "Localization from the event",
        "start_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00",
        "end_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00"
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