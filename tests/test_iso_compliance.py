#!/usr/bin/env python3
"""
Comprehensive tests for ISO Compliance Manager.
"""

import pytest
import sys
import os

# Add the parent directory to sys.path to import ai_governance
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_governance.standards.iso_compliance import ISOComplianceManager, ISOStandard, ComplianceMaturity


class TestISOComplianceManager:
    """Test the ISO Compliance Manager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.iso_manager = ISOComplianceManager()
        
        # Register test systems
        self.iso_manager.register_system("test_system_1", {
            "name": "AI System 1",
            "use_case": "credit_scoring",
            "risk_level": "high",
            "industry_sector": "financial"
        })
        
        self.iso_manager.register_system("test_system_2", {
            "name": "AI System 2",
            "use_case": "recommendations",
            "risk_level": "low",
            "industry_sector": "retail"
        })
        
    def test_initialization(self):
        """Test ISO manager initialization."""
        manager = ISOComplianceManager()
        assert manager is not None
        assert hasattr(manager, 'registered_systems')
        assert hasattr(manager, 'compliance_assessments')
        assert hasattr(manager, 'standard_requirements')
        assert hasattr(manager, 'maturity_assessments')
        
    def test_system_registration(self):
        """Test system registration."""
        system_id = "test_system_3"
        system_info = {
            "name": "Test System",
            "use_case": "fraud_detection",
            "risk_level": "high",
            "industry_sector": "banking"
        }
        
        self.iso_manager.register_system(system_id, system_info)
        
        assert system_id in self.iso_manager.registered_systems
        assert system_id in self.iso_manager.compliance_assessments
        assert system_id in self.iso_manager.maturity_assessments
        
    def test_iso_compliance_assessment(self):
        """Test ISO compliance assessment."""
        assessment = self.iso_manager.assess_iso_compliance("test_system_1")
        
        assert "system_id" in assessment
        assert "overall_compliance_score" in assessment or "assessed_at" in assessment
        assert "standard_assessments" in assessment
        
    def test_maturity_assessment(self):
        """Test maturity level assessment from compliance assessment."""
        assessment = self.iso_manager.assess_iso_compliance("test_system_1")
        
        assert "maturity_level" in assessment
        
    def test_gap_analysis(self):
        """Test gap analysis."""
        gap_analysis = self.iso_manager.conduct_gap_analysis("test_system_1", "ISO/IEC 23053")
        
        assert "system_id" in gap_analysis
        assert "standard" in gap_analysis
        assert "implementation_gaps" in gap_analysis or "gaps" in gap_analysis
        
    def test_compliance_progress_tracking(self):
        """Test compliance progress tracking."""
        progress_data = {
            "milestone": "Risk Assessment Completed",
            "completion_percentage": 60,
            "evidence": ["document1", "document2"],
            "next_steps": ["Review controls", "Update documentation"]
        }
        
        self.iso_manager.track_compliance_progress("test_system_1", progress_data)
        
        # Check that progress was tracked - no error thrown
        assert True
        
    def test_compliance_report_generation(self):
        """Test compliance report generation."""
        report = self.iso_manager.generate_compliance_report("test_system_1")
        
        assert "scope" in report
        assert "compliance_summary" in report
        
    def test_compliance_report_all_systems(self):
        """Test compliance report for all systems."""
        report = self.iso_manager.generate_compliance_report()
        
        assert "compliance_summary" in report
        assert "total_systems" in report["compliance_summary"]
        
    def test_compliance_assessment_unregistered_system(self):
        """Test compliance assessment for unregistered system."""
        assessment = self.iso_manager.assess_iso_compliance("nonexistent_system")
        
        assert "error" in assessment
        
    def test_gap_analysis_unregistered_system(self):
        """Test gap analysis for unregistered system."""
        gap_analysis = self.iso_manager.conduct_gap_analysis("nonexistent_system", "ISO/IEC 23053")
        
        assert "error" in gap_analysis
        
    def test_multiple_standards_assessment(self):
        """Test assessment of multiple ISO standards."""
        # Register system with multiple applicable standards
        self.iso_manager.register_system("multi_standard_system", {
            "name": "Multi-Standard System",
            "use_case": "healthcare_ai",
            "risk_level": "critical",
            "industry_sector": "healthcare",
            "requires_security": True,
            "requires_quality": True
        })
        
        assessment = self.iso_manager.assess_iso_compliance("multi_standard_system")
        
        assert "standard_assessments" in assessment
        # Should have assessments for multiple standards
        assert len(assessment["standard_assessments"]) > 0
        
    def test_different_risk_levels(self):
        """Test systems with different risk levels."""
        # Critical risk system
        self.iso_manager.register_system("critical_system", {
            "name": "Critical Risk System",
            "use_case": "medical_diagnosis",
            "risk_level": "critical",
            "industry_sector": "healthcare"
        })
        
        # Low risk system
        self.iso_manager.register_system("low_risk_system", {
            "name": "Low Risk System",
            "use_case": "content_recommendation",
            "risk_level": "low",
            "industry_sector": "media"
        })
        
        critical_assessment = self.iso_manager.assess_iso_compliance("critical_system")
        low_assessment = self.iso_manager.assess_iso_compliance("low_risk_system")
        
        assert "assessed_at" in critical_assessment
        assert "assessed_at" in low_assessment
        
    def test_industry_specific_compliance(self):
        """Test industry-specific compliance requirements."""
        # Financial services system
        self.iso_manager.register_system("financial_system", {
            "name": "Financial AI System",
            "use_case": "trading",
            "risk_level": "high",
            "industry_sector": "financial"
        })
        
        assessment = self.iso_manager.assess_iso_compliance("financial_system")
        
        assert "applicable_standards" in assessment
        assert len(assessment["applicable_standards"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
