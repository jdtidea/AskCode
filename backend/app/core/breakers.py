from datetime import timedelta

from aiobreaker import CircuitBreaker

# TODO: Move these values to external config
max_failures = 5
timeout_duration = timedelta(seconds=30)


bne_breaker = CircuitBreaker(fail_max=max_failures, timeout_duration=timeout_duration)
domains_breaker = CircuitBreaker(
    fail_max=max_failures, timeout_duration=timeout_duration
)
health_library_breaker = CircuitBreaker(
    fail_max=max_failures, timeout_duration=timeout_duration
)
vcm_breaker = CircuitBreaker(fail_max=max_failures, timeout_duration=timeout_duration)
entity_breaker = CircuitBreaker(
    fail_max=max_failures, timeout_duration=timeout_duration
)
