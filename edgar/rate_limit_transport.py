from ratemate import RateLimit
import httpx

rate_limit = RateLimit(max_count=10, per=1)  # 10 requests per 1 seconds

class RateLimitTransport(httpx.BaseTransport):
    def __init__(self, **kwargs):
        self._wrapper = httpx.HTTPTransport(**kwargs)

    def handle_request(self, request):
        # Wait for any existing rate limits
        rate_limit.wait()
        response = self._wrapper.handle_request(request)
        return response

    def close(self):
        self._wrapper.close()