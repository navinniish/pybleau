"""
pybleau - A Python library for Tableau REST and Metadata APIs
"""

__version__ = "0.1.0"

# Import main classes for easier access
from .auth import TableauClient

__all__ = ['TableauClient']
