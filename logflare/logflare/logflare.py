import requests
from threading import Timer
from datetime import datetime
class LogflareLogger:
    def __init__(self, api_key, drain_id, flush_interval=5, app_name=None, base_url=None) -> None:
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = "https://api.logflare.app/api/logs"


        self.url = self.base_url + "?source="+drain_id
        
        self.headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
        }
        
        self.buffer = []
        self.app = app_name
        self.flush_interval = flush_interval
        self.timer = None

    def exit(self):
        self.flush()
        if self.timer and self.timer.is_alive():
            self.timer.cancel()
    
    
    def error(self, message, ):
        self._log(message, "ERROR")

    def warning(self, message, ):
        self._log(message, "WARNING")

    def info(self, message):
        self._log(message, "INFO")
        

    def _log(self, message, loggingLevel, code=None):
        metadata = {
            "time_str": str(datetime.utcnow())
        }

        if self.app:
            metadata["app"] = self.app
        
        if loggingLevel:
            metadata["loggingLevel"] = loggingLevel
        
        if code:
            metadata["code"] = code

    

        payload = {
            "message": message,
            "metadata": metadata,
        }
        self.buffer.append(payload)
        
        if not self.timer or not self.timer.is_alive():
            print("Starting timer")
            self.timer = Timer(self.flush_interval, self.flush)
            self.timer.start()

    def flush(self):
        if len(self.buffer) > 0:
            print("Flushing")
            print({
                "batch":self.buffer
            })
            response = requests.post(self.url, headers=self.headers, json={
                "batch":self.buffer
            })
            self.buffer = []
            print("logflare", response.content)
      