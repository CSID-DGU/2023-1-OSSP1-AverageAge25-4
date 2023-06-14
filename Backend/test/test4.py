email = "test@test.com"
token = generate_token()
expected_link = ""
result = generate_verification_link(email, token)