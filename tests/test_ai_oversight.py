#!/usr/bin/env python3
"""
Comprehensive tests for AI Oversight Manager.
"""

import pytest
import sys
import os

# Add the parent directory to sys.path to import ai_governance
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_governance.core.ai_oversight import AIOversightManager, OversightLevel, DecisionType


class TestAIOversightManager:
    """Test the AI Oversight Manager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.oversight_manager = AIOversightManager()
        
        # Register test systems with different oversight levels
        self.oversight_manager.register_system("test_system_1", {
            "name": "Low Risk System",
            "use_case": "testing",
            "risk_level": "low",
            "decision_impact": "low"
        })
        
        self.oversight_manager.register_system("test_system_2", {
            "name": "High Risk System",
            "use_case": "credit_scoring",
            "risk_level": "high",
            "decision_impact": "high",
            "requires_human_review": True
        })
        
    def test_initialization(self):
        """Test oversight manager initialization."""
        manager = AIOversightManager()
        assert manager is not None
        assert hasattr(manager, 'registered_systems')
        assert hasattr(manager, 'audit_trails')
        assert hasattr(manager, 'decision_logs')
        assert hasattr(manager, 'oversight_reports')
        
    def test_system_registration(self):
        """Test system registration."""
        system_id = "test_system_3"
        system_info = {
            "name": "Test System",
            "use_case": "testing",
            "risk_level": "medium"
        }
        
        self.oversight_manager.register_system(system_id, system_info)
        
        assert system_id in self.oversight_manager.registered_systems
        assert system_id in self.oversight_manager.audit_trails
        assert system_id in self.oversight_manager.decision_logs
        
    def test_oversight_compliance_assessment(self):
        """Test oversight compliance assessment."""
        assessment = self.oversight_manager.assess_oversight_compliance("test_system_1")
        
        assert "system_id" in assessment
        assert "score" in assessment
        assert "compliance_areas" in assessment
        assert assessment["score"] >= 0
        assert assessment["score"] <= 100
        
    def test_log_decision(self):
        """Test decision logging."""
        decision_data = {
            "decision_type": "automated",
            "input_data": {"amount": 5000},
            "output": {"approved": True},
            "confidence": 0.95,
            "timestamp": "2024-01-01T00:00:00",
            "explanation": "High confidence decision"
        }
        
        self.oversight_manager.log_decision("test_system_1", decision_data)
        
        assert len(self.oversight_manager.decision_logs["test_system_1"]) > 0
        logged_decision = self.oversight_manager.decision_logs["test_system_1"][-1]
        assert "decision_id" in logged_decision
        assert logged_decision["confidence"] == 0.95
        
    def test_transparency_report_generation(self):
        """Test transparency report generation."""
        # Log some decisions first
        for i in range(5):
            decision_data = {
                "decision_type": "automated",
                "output": {"approved": i % 2 == 0},
                "confidence": 0.8 + (i * 0.03),
                "explanation": f"Decision {i}",
                "human_reviewer": "reviewer_1" if i % 3 == 0 else None,
                "timestamp": f"2024-01-0{i+1}T00:00:00"
            }
            self.oversight_manager.log_decision("test_system_1", decision_data)
        
        report = self.oversight_manager.generate_transparency_report("test_system_1")
        
        assert "system_id" in report
        assert "period" in report
        assert "summary" in report
        assert "compliance_metrics" in report
        
    def test_audit_trail_retrieval(self):
        """Test audit trail retrieval."""
        # Log some decisions
        decision_data = {
            "decision_type": "automated",
            "output": {"approved": True},
            "confidence": 0.9
        }
        self.oversight_manager.log_decision("test_system_1", decision_data)
        
        audit_trail = self.oversight_manager.get_audit_trail("test_system_1")
        
        assert "system_id" in audit_trail
        assert "events" in audit_trail
        assert "total_events" in audit_trail
        assert len(audit_trail["events"]) > 0
        
    def test_audit_trail_with_event_type_filter(self):
        """Test audit trail retrieval with event type filter."""
        audit_trail = self.oversight_manager.get_audit_trail("test_system_1", event_type="system_registered")
        
        assert "system_id" in audit_trail
        assert "events" in audit_trail
        
    def test_audit_trail_with_limit(self):
        """Test audit trail retrieval with limit."""
        # Log multiple decisions
        for i in range(10):
            decision_data = {
                "decision_type": "automated",
                "output": {"approved": True},
                "confidence": 0.9
            }
            self.oversight_manager.log_decision("test_system_1", decision_data)
        
        audit_trail = self.oversight_manager.get_audit_trail("test_system_1", limit=5)
        
        assert len(audit_trail["events"]) <= 5
        
    def test_decision_escalation(self):
        """Test decision escalation."""
        # Log a decision
        decision_data = {
            "decision_type": "automated",
            "output": {"approved": True},
            "confidence": 0.65  # Low confidence for escalation
        }
        self.oversight_manager.log_decision("test_system_2", decision_data)
        
        decision_id = self.oversight_manager.decision_logs["test_system_2"][-1]["decision_id"]
        
        self.oversight_manager.escalate_decision(
            "test_system_2",
            decision_id,
            "Low confidence score",
            "supervisor_1"
        )
        
        # Check that escalation was logged in audit trail
        audit_trail = self.oversight_manager.get_audit_trail("test_system_2")
        escalation_events = [e for e in audit_trail["events"] if e["event_type"] == "decision_escalated"]
        assert len(escalation_events) > 0
        
    def test_transparency_report_with_date_range(self):
        """Test transparency report with date range."""
        # Log decisions with timestamps
        decision_data = {
            "decision_type": "automated",
            "output": {"approved": True},
            "confidence": 0.9,
            "explanation": "Test decision",
            "timestamp": "2024-06-15T00:00:00"
        }
        self.oversight_manager.log_decision("test_system_1", decision_data)
        
        report = self.oversight_manager.generate_transparency_report(
            "test_system_1",
            start_date="2024-01-01",
            end_date="2024-12-31"
        )
        
        assert "system_id" in report or "error" in report
        
    def test_compliance_assessment_unregistered_system(self):
        """Test compliance assessment for unregistered system."""
        assessment = self.oversight_manager.assess_oversight_compliance("nonexistent_system")
        
        assert "error" in assessment
        
    def test_transparency_report_no_decisions(self):
        """Test transparency report when no decisions logged."""
        # Register new system without logging decisions
        self.oversight_manager.register_system("test_system_empty", {
            "name": "Empty System",
            "use_case": "testing"
        })
        
        report = self.oversight_manager.generate_transparency_report("test_system_empty")
        
        # Should return error when no decisions
        assert "error" in report
        
    def test_multiple_decision_logging(self):
        """Test logging multiple decisions with various attributes."""
        # Log decisions with different characteristics
        decisions = [
            {
                "decision_type": "automated",
                "output": {"approved": True},
                "confidence": 0.95,
                "explanation": "High confidence",
                "risk_level": "low",
                "timestamp": "2024-01-01T00:00:00"
            },
            {
                "decision_type": "human_in_loop",
                "output": {"approved": False},
                "confidence": 0.65,
                "explanation": "Needs review",
                "human_reviewer": "reviewer_1",
                "risk_level": "medium",
                "timestamp": "2024-01-02T00:00:00"
            },
            {
                "decision_type": "automated",
                "output": {"approved": True},
                "confidence": 0.88,
                "explanation": "Standard approval",
                "risk_level": "low",
                "timestamp": "2024-01-03T00:00:00"
            }
        ]
        
        for decision in decisions:
            self.oversight_manager.log_decision("test_system_1", decision)
        
        assert len(self.oversight_manager.decision_logs["test_system_1"]) >= 3
        
        # Generate report to check analytics
        report = self.oversight_manager.generate_transparency_report("test_system_1")
        assert report["summary"]["total_decisions"] >= 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
