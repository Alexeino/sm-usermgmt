### Creating a User
```
curl -X 'POST' \
  'http://localhost:8000/api/v1/users/create' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "Raju",
  "email": "raju@test.com",
  "role": "admin",
  "password": "admin123"
}'
```