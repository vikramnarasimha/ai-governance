"""
AI Governance Tool for Financial Services Institutions

This package provides comprehensive AI governance capabilities including:
- Model Risk Management
- AI Oversight
- Data Governance
- Data Residency Management
- ISO Standards Compliance
"""

__version__ = "0.1.0"
__author__ = "AI Governance Team"

from .core import GovernanceFramework
from .workflows import WorkflowOrchestrator

__all__ = [
    "GovernanceFramework",
    "WorkflowOrchestrator",
]