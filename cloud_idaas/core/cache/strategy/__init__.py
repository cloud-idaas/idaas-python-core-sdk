"""
IDaaS Python SDK - Cache Strategy Module

This module provides prefetch strategy implementations.
"""

from cloud_idaas.core.cache.strategy.non_blocking_prefetch_strategy import NonBlockingPrefetchStrategy
from cloud_idaas.core.cache.strategy.one_caller_blocks_prefetch_strategy import OneCallerBlocksPrefetchStrategy

__all__ = [
    "OneCallerBlocksPrefetchStrategy",
    "NonBlockingPrefetchStrategy",
]
