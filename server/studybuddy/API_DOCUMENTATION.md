# 📖 StuddyBuddy API Documentation

---

## Authentication & User

### POST `/api/v1/auth/signup/`
**Body:**
```json
{
  "email": "user@example.com",
  "username": "user123",
  "password": "yourpassword",
  "is_student": true,
  "is_senior": false,
  "profile_image": "<file>" // optional, multipart/form-data
}
```
**Response:**
`201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "user123",
  "is_student": true,
  "is_senior": false,
  "friends": [],
  "profile_image": "/media/profile_images/..."
}
```

### POST `/api/v1/auth/login/`
**Body:**
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```
**Response:**
`200 OK`
```json
{
  "token": "<jwt_token>",
  "user": { ... }
}
```

### POST `/api/v1/auth/logout/`
**Headers:**
`Authorization: Bearer <token>`
**Response:**
`200 OK`
```json
{ "detail": "Logged out successfully." }
```

### POST `/api/v1/auth/password-reset/`
**Body:**
```json
{ "email": "user@example.com" }
```
**Response:**
`200 OK`
```json
{ "detail": "Password reset email sent." }
```

### POST `/api/v1/auth/email-verify/`
**Body:**
```json
{ "email": "user@example.com" }
```
**Response:**
`200 OK`
```json
{ "detail": "Verification email sent." }
```

### GET `/api/v1/auth/profile/`
**Headers:**
`Authorization: Bearer <token>`
**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "user123",
    "is_student": true,
    "is_senior": false,
    "friends": [ ... ],
    "profile_image": "/media/profile_images/..."
  },
  "friend_requests": [ ... ]
}
```

### PUT `/api/v1/auth/profile/update/`
**Headers:**
`Authorization: Bearer <token>`
**Body:**
Any updatable user fields (see signup).
**Response:**
Updated user object.

### POST `/api/v1/auth/accept_friend_request/<request_id>/`
### POST `/api/v1/auth/decline_friend_request/<request_id>/`
**Headers:**
`Authorization: Bearer <token>`
**Response:**
```json
{ "message": "Friend request accepted/declined successfully" }
```

---

## Notes

### GET `/api/v1/notes/`
**Headers:**
`Authorization: Bearer <token>`
**Query:**
`?search=...&ordering=...`
**Response:**
Paginated list of notes:
```json
{
  "count": 1,
  "results": [
    {
      "id": "uuid",
      "title": "Note Title",
      "content": "Text content",
      "rich_text_content": "Rich text",
      "drawing": "...",
      "created_by": 1,
      "shared_with": [2, 3],
      "last_modified_by": 1
    }
  ]
}
```

### POST `/api/v1/notes/create/`
**Body:**
```json
{
  "title": "Note Title",
  "content": "Text content",
  "rich_text_content": "Rich text",
  "drawing": "...",
  "shared_with": [2, 3]
}
```
**Response:**
Created note object.

### GET `/api/v1/notes/<uuid:pk>/`
**Response:**
Note detail.

### POST `/api/v1/notes/<uuid:pk>/share/`
**Body:**
```json
{ "shared_with": [2, 3] }
```
**Response:**
Updated note object.

### PUT `/api/v1/notes/<uuid:pk>/update/`
**Body:**
Any updatable note fields.
**Response:**
Updated note object.

### DELETE `/api/v1/notes/<uuid:pk>/delete/`
**Response:**
```json
{ "message": "Note deleted successfully" }
```

---

## Test Series

### GET `/api/v1/testseries/subjects/`
**Response:**
List of subjects.

### GET `/api/v1/testseries/subdomains/<subject_id>/`
**Response:**
List of subdomains for subject.

### GET `/api/v1/testseries/chapters/<subdomain_id>/`
**Response:**
List of chapters for subdomain.

### GET `/api/v1/testseries/questions/<chapter_ids>/`
**Response:**
List of questions for chapters.

### POST `/api/v1/testseries/generate_test/`
**Body:**
```json
{
  "chapter_ids": [1, 2, 3],
  "duration": 30
}
```
**Response:**
Created test object.

### POST `/api/v1/testseries/submit_test/<test_id>/`
**Body:**
```json
{ "answers": [ ... ] }
```
**Response:**
Test result.

### GET `/api/v1/testseries/get_test_result/<test_id>/`
**Response:**
Test and answers.

### GET `/api/v1/testseries/get_previous_tests/`
**Response:**
List of previous tests.

### GET `/api/v1/testseries/get_test_detail/<test_id>/`
**Response:**
Test detail.

### GET `/api/v1/testseries/analysis/performance/`
**Response:**
Performance summary.

---

## Todo List

### GET `/api/v1/todolist/assignments/`
**Headers:**
`Authorization: Bearer <token>`
**Response:**
Paginated list of assignments.

### POST `/api/v1/todolist/create_assignments/`
**Body:**
```json
{
  "subject": "Math",
  "chapter": "Algebra",
  "deadline": "2024-07-20T23:59:00Z"
}
```
**Response:**
Created assignment.

### GET `/api/v1/todolist/selfstudy/`
**Response:**
Paginated list of self-study items.

### POST `/api/v1/todolist/create_selfstudy/`
**Body:**
```json
{
  "subject": "Physics",
  "deadline": "2024-07-20T23:59:00Z"
}
```
**Response:**
Created self-study item.

### POST `/api/v1/todolist/complete_assignments/<uuid>/`
### POST `/api/v1/todolist/complete_selfstudy/<uuid>/`
**Response:**
```json
{ "message": "Assignment/Self-study marked as completed" }
```

### DELETE `/api/v1/todolist/delete_assignments/<uuid>/`
### DELETE `/api/v1/todolist/delete_selfstudy/<uuid>/`
**Response:**
```json
{ "message": "Assignment/Self-study deleted" }
```

---

## Resources

### GET `/api/v1/resources/`
**Response:**
```json
[
  {
    "id": 1,
    "title": "Resource Title",
    "url": "http://...",
    "pdf_file": "/media/resources/...",
    "resource_type": "pdf"
  }
]
```

---

## PDF Chatbot

### POST `/api/v1/pdfchatbot/upload_pdfs/`
**Body:**
`multipart/form-data` with PDF file(s)
**Response:**
```json
{ "message": "PDF uploaded successfully" }
```

### POST `/api/v1/pdfchatbot/ask_question/`
**Body:**
```json
{ "question": "What is ...?", "pdf_id": 1 }
```
**Response:**
```json
{ "answer": "..." }
```

### POST `/api/v1/pdfchatbot/chat/`
**Body:**
```json
{ "message": "..." }
```
**Response:**
```json
{ "response": "..." }
```

---

## Connections

### POST `/api/v1/connect/send_friend_request/<receiver_id>/`
**Response:**
```json
{ "message": "Friend request sent" }
```

### GET `/api/v1/connect/friends/`
**Response:**
List of friends.

### GET `/api/v1/connect/meeting/`
### GET `/api/v1/connect/joinmeet/`
**Response:**
Meeting info.

### GET `/api/v1/connect/chat/<username>/`
**Response:**
Chat history.

---

## Admin/Analytics

### GET `/api/v1/auth/admin/role-counts/`
### GET `/api/v1/auth/admin/active-users/`
### GET `/api/v1/auth/admin/recent-signups/`
### POST `/api/v1/auth/admin/deactivate/<user_id>/`
### POST `/api/v1/auth/admin/reactivate/<user_id>/`
### GET `/api/v1/auth/admin/export/<user_id>/`
**Headers:**
`Authorization: Bearer <admin_token>`
**Response:**
User/admin analytics or user data.

---

## Health & Monitoring

### GET `/health/`
**Response:**
```json
{ "status": "ok" }
```

### GET `/metrics/`
**Response:**
Prometheus metrics.

---

## General Notes
- All endpoints require `Authorization: Bearer <token>` unless for signup/login.
- All list endpoints support pagination, search, and ordering where applicable.
- All file uploads use `multipart/form-data`.
- All error responses are standardized:
```json
{
  "error": { ... },
  "status_code": 400
}
```

---

**For full, interactive API docs, visit `/swagger/` or `/redoc/` on your running backend.** 