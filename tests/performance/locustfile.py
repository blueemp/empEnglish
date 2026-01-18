# Performance tests using Locust
# File path: tests/performance/locustfile.py

from locust import HttpUser, task, between


class EmpEnglishUser(HttpUser):
    """Simulates user behavior for empEnglish platform"""

    wait_time = between(1, 3)
    host = "http://localhost:8000"

    @task(3)
    def get_health_check(self):
        """Health check - frequently called"""
        self.client.get("/health")

    @task(1)
    def wechat_login(self):
        """WeChat login - less frequent"""
        # This would need a real WeChat code in production
        self.client.post("/api/v1/auth/wechat/login", json={"code": "test_code"})

    @task(2)
    def list_questions(self):
        """List questions - user browsing"""
        self.client.get("/api/v1/questions?page=1&page_size=20")

    @task(1)
    def get_user_profile(self):
        """Get user profile - requires auth"""
        # In production, this would need a valid token
        # headers = {"Authorization": "Bearer <token>"}
        self.client.get("/api/v1/users/profile")


class EmpEnglishStudentUser(HttpUser):
    """Simulates student practice session behavior"""

    wait_time = between(5, 10)

    def on_start(self):
        """Called when a user starts - create practice session"""
        # In production: self.client.post("/api/v1/practice/sessions", ...)
        self.session_id = "test_session_id"

    @task(3)
    def get_next_question(self):
        """Get next question in practice"""
        self.client.get(f"/api/v1/practice/sessions/{self.session_id}/next")

    @task(2)
    def submit_answer(self):
        """Submit answer to practice session"""
        self.client.post(
            f"/api/v1/practice/sessions/{self.session_id}/turns/test_turn/submit",
            json={
                "answer_text": "This is a test answer for the question.",
                "audio_url": "http://example.com/audio.wav",
            },
        )

    @task(1)
    def get_practice_report(self):
        """Get practice report"""
        self.client.get(f"/api/v1/practice/sessions/{self.session_id}/report")


class LoadTestShapes:
    """Different load test scenarios"""

    # Scenario 1: Light load - mostly reads
    LIGHT_LOAD = {"users": 10, "spawn_rate": 1, "duration": "2m"}

    # Scenario 2: Medium load - mixed reads and writes
    MEDIUM_LOAD = {"users": 50, "spawn_rate": 5, "duration": "5m"}

    # Scenario 3: Heavy load - stress test
    HEAVY_LOAD = {"users": 100, "spawn_rate": 10, "duration": "10m"}

    # Scenario 4: Spike test - sudden traffic increase
    SPIKE_TEST = {"users": 200, "spawn_rate": 50, "duration": "1m"}


# Expected response time thresholds (in milliseconds)
RESPONSE_TIME_THRESHOLDS = {
    "health_check": 50,
    "list_questions": 200,
    "get_question": 100,
    "login": 500,
    "submit_answer": 1000,  # Longer due to AI processing
    "get_report": 300,
}


# Expected error rate thresholds
ERROR_RATE_THRESHOLDS = {
    "max_error_rate": 0.05,  # 5% max error rate
    "critical_error_rate": 0.01,  # 1% critical error rate
}
