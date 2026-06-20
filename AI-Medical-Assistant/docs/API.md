# API Documentation

Base URL: `http://127.0.0.1:8000`

## Authentication

### POST `/api/auth/register`
Creates a user account. The first registered user becomes an admin.

Request:
```json
{
  "full_name": "Dr. Tanya Gupta",
  "email": "doctor@example.com",
  "password": "secure123"
}
```

### POST `/api/auth/login`
Returns a JWT bearer token.

Request:
```json
{
  "email": "doctor@example.com",
  "password": "secure123"
}
```

## Scans

All scan endpoints require `Authorization: Bearer <token>`.

### POST `/api/scans/analyze`
Multipart upload field: `file`. Accepted formats: JPG, JPEG, PNG.

Response includes prediction label, confidence, risk level, image path, heatmap path, and timestamp.

### GET `/api/scans/history`
Returns the authenticated user's scan history.

### GET `/api/scans/analytics`
Returns total scans, class distribution, average confidence, and seven-day trend data.

### GET `/api/scans/{scan_id}/image`
Streams the original uploaded image.

### GET `/api/scans/{scan_id}/heatmap`
Streams the Grad-CAM overlay image.

### GET `/api/scans/{scan_id}/report`
Downloads a PDF report.

### GET `/api/scans/exports/history.csv`
Downloads scan history as CSV.

## Admin

Admin endpoints require an admin JWT.

### GET `/api/admin/users`
Lists all users.

### GET `/api/admin/scans?search=term`
Lists and searches all scan records.

### DELETE `/api/admin/scans/{scan_id}`
Deletes a scan record and its generated files.
