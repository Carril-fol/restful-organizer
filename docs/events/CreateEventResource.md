## Create events
Allows to the users create events.

**URL**: localhost:[PORT]/events/api/v1/<folder_id>

**Method**: `POST`

**Authentication**: Required

## Application data:
```bash
{
    "name_event": "Name for the event",
    "localization": "Localization from the event",
    "start_date": "Date in the format: YYYY-MM-DD (e.g., 2024-07-20) or YYYY-MM-DDTHH:MM:SS (e.g., 2024-07-20T14:30:00). 
        For formats including milliseconds and timezone, use: YYYY-MM-DDTHH:MM:SS.MS+00:00 (e.g., 2024-07-20T14:30:00.123+00:00).",
     "end_date": "Date in the format: YYYY-MM-DD (e.g., 2024-07-20) or YYYY-MM-DDTHH:MM:SS (e.g., 2024-07-20T14:30:00). 
        For formats including milliseconds and timezone, use: YYYY-MM-DDTHH:MM:SS.MS+00:00 (e.g., 2024-07-20T14:30:00.123+00:00)."
}
```

## Success response
**Code**: `200 OK`

**Content**:
```bash
{
    "status": "Created",
    "event": {
        "name_event": "Name for the event",
        "folder_id": "Id from the folder",
        "localization": "Localization from the event",
        "start_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00",
        "end_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00"
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