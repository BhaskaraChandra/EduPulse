
class appConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(appConfig, cls).__new__(cls)
            cls._instance.init_config()
        return cls._instance

    def init_config(self):
        self.local_service = True
        self.base_urls = {
            "questions": "https://epsvc-qt.onrender.com/",
            "users": "https://epsvc-u.onrender.com/",
            "metrics": "https://epsvc-m.onrender.com/",
            "tests": "https://epsvc-qt.onrender.com/"
        }
        if self.local_service:
            self.base_urls = {
                "questions": "http://localhost:9117/",
                "users": "http://localhost:9117/",
                "metrics": "http://localhost:9117/",
                "tests": "http://localhost:9117/"
            }

    @property
    def questions_service_url(self):
        return self.base_urls["questions"]

    @property
    def users_service_url(self):
        return self.base_urls["users"]
    
    @property
    def metrics_service_url(self):
        return self.base_urls["metrics"]
    
    @property
    def tests_service_url(self):
        return self.base_urls["tests"]
