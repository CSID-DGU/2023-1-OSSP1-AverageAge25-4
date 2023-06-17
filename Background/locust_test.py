from locust import HttpUser, between, task

class MyUser(HttpUser):
    wait_time = between(1, 2)  # Add some delay between requests

    def on_start(self):
        self.get_csrf_token()  # Obtain the CSRF token before login



    def get_csrf_token(self):
        response = self.client.get("/login/")  # Make a GET request to obtain the CSRF token
        csrf_token = response.cookies['csrftoken']  # Extract the CSRF token from the response cookies
        self.client.headers['X-CSRFToken'] = csrf_token  # Set the CSRF token in the headers

    @task
    def login(self):
        response = self.client.post(
            "/login/",  # Endpoint for login
            json={
                "uid": "dpsxj0618@naver.com",
                "password": "12341234"
            }
        )
        if response.status_code == 200:
            print("Login successful!")
        else:
            print("Login failed!")