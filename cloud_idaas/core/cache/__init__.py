"""
IDaaS Python SDK - Cache Module

This module provides caching functionality for the SDK, including
time-based caching with expiration checking and prefetching strategies.
"""

from cloud_idaas.core.cache.cached_result_supplier import CachedResultSupplier
from cloud_idaas.core.cache.prefetch_strategy import PrefetchStrategy
from cloud_idaas.core.cache.refresh_result import RefreshResult, RefreshResultBuilder
from cloud_idaas.core.cache.stale_value_behavior import StaleValueBehavior
from cloud_idaas.core.cache.strategy.non_blocking_prefetch_strategy import NonBlockingPrefetchStrategy
from cloud_idaas.core.cache.strategy.one_caller_blocks_prefetch_strategy import OneCallerBlocksPrefetchStrategy

__all__ = [
    "CachedResultSupplier",
    "PrefetchStrategy",
    "RefreshResult",
    "RefreshResultBuilder",
    "StaleValueBehavior",
    "NonBlockingPrefetchStrategy",
    "OneCallerBlocksPrefetchStrategy",
]
