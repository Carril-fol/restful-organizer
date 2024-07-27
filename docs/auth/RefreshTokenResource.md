## Refresh Token
Allows to create a new access token from a refresh token.

**URL**: localhost:[PORT]/users/api/v1/refresh

**Method**: `POST`

**Authentication**: Required

**Header Authorization:**:
```bash
{
    Authorization: "8uP9dv0czfTLY8WEma1fZyBYLzUedsX.iwp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
}
```

## Success response
**Code**: `200 OK`

**Content**:
```bash
{
    "access_token": "8aP9dv0czfTLY8WEma1fZyBYLzUedsXdsdp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
}
```

## Error response
**Condition**: Missing Authorization Header.

**Code**: `400 BAD REQUEST`

**Content**:
```bash
{
    "msg": "Missing Authorization Header"
}
```