existing_user_id = 1
not_existing_user_id = 99999

data_for_post = {
    "name": "Test User",
    "username": "testuser",
    "email": "test@example.com"
}

data_for_update = {
    "name": "Updated Name",
    "username": "updateduser",
    "email": "updated@example.com"
}

# для теста "успешная регистрация" (POST /users)
complete_creds = {
    "name": "Eve Holt",
    "username": "eveholt",
    "email": "eve.holt@example.com"
}
