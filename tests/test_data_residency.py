#!/usr/bin/env python3
"""
Comprehensive tests for Data Residency Manager.
"""

import pytest
import sys
import os

# Add the parent directory to sys.path to import ai_governance
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_governance.core.data_residency import DataResidencyManager, DataSovereigntyLevel, ComplianceStatus


class TestDataResidencyManager:
    """Test the Data Residency Manager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.residency_manager = DataResidencyManager()
        
        # Register test systems
        self.residency_manager.register_system("test_system_1", {
            "name": "EU Data System",
            "jurisdictions": ["EU", "Germany"],
            "data_types": ["pii", "financial"],
            "cloud_provider": "aws",
            "data_sensitivity": "high"
        })
        
        self.residency_manager.register_system("test_system_2", {
            "name": "US Data System",
            "jurisdictions": ["US"],
            "data_types": ["analytics"],
            "cloud_provider": "gcp",
            "data_sensitivity": "low"
        })
        
    def test_initialization(self):
        """Test residency manager initialization."""
        manager = DataResidencyManager()
        assert manager is not None
        assert hasattr(manager, 'registered_systems')
        assert hasattr(manager, 'residency_policies')
        assert hasattr(manager, 'compliance_assessments')
        assert hasattr(manager, 'data_locations')
        
    def test_system_registration(self):
        """Test system registration."""
        system_id = "test_system_3"
        system_info = {
            "name": "Test System",
            "jurisdictions": ["UK"],
            "data_types": ["customer"],
            "cloud_provider": "azure"
        }
        
        self.residency_manager.register_system(system_id, system_info)
        
        assert system_id in self.residency_manager.registered_systems
        assert system_id in self.residency_manager.compliance_assessments
        
    def test_residency_compliance_assessment(self):
        """Test residency compliance assessment."""
        assessment = self.residency_manager.assess_residency_compliance("test_system_1")
        
        assert "system_id" in assessment
        assert "score" in assessment
        assert "compliance_areas" in assessment
        assert assessment["score"] >= 0
        assert assessment["score"] <= 100
        
    def test_data_location_tracking(self):
        """Test data location tracking."""
        location_data = {
            "region": "eu-west-1",
            "country": "Germany",
            "data_center": "FRA-DC-01",
            "data_types": ["pii", "financial"],
            "storage_type": "primary",
            "timestamp": "2024-01-01T00:00:00"
        }
        
        self.residency_manager.track_data_location("test_system_1", location_data)
        
        assert "test_system_1" in self.residency_manager.data_locations
        
    def test_residency_policy_update(self):
        """Test residency policy update."""
        policy_data = {
            "name": "EU Data Residency Policy",
            "description": "All EU data must remain in EU",
            "jurisdictions": ["EU"],
            "allowed_regions": ["eu-west-1", "eu-central-1"],
            "restricted_regions": ["us-east-1", "ap-south-1"],
            "requirements": ["encryption_at_rest", "encryption_in_transit"]
        }
        
        self.residency_manager.update_residency_policy("eu_policy", policy_data)
        
        assert "eu_policy" in self.residency_manager.residency_policies
        
    def test_residency_report_generation(self):
        """Test residency report generation."""
        # First do an assessment to create data
        self.residency_manager.assess_residency_compliance("test_system_1")
        
        report = self.residency_manager.get_residency_report("test_system_1")
        
        assert "scope" in report
        assert "compliance_summary" in report
        assert "system_details" in report
        
    def test_residency_report_all_systems(self):
        """Test residency report for all systems."""
        report = self.residency_manager.get_residency_report()
        
        assert "compliance_summary" in report
        assert "total_systems" in report["compliance_summary"]
        assert "system_details" in report
        
    def test_data_transfer_validation_compliant(self):
        """Test data transfer validation for compliant transfer."""
        validation = self.residency_manager.validate_data_transfer(
            from_region="eu-west-1",
            to_region="eu-central-1",
            data_types=["pii"],
            system_id="test_system_1"
        )
        
        assert "is_compliant" in validation
        assert "from_region" in validation
        assert "to_region" in validation
        assert "data_types" in validation
        
    def test_data_transfer_validation_non_compliant(self):
        """Test data transfer validation for non-compliant transfer."""
        validation = self.residency_manager.validate_data_transfer(
            from_region="eu-west-1",
            to_region="us-east-1",
            data_types=["pii", "financial"],
            system_id="test_system_1"
        )
        
        assert "is_compliant" in validation
        assert "violations" in validation
        
    def test_data_transfer_validation_without_system_id(self):
        """Test data transfer validation without system ID."""
        validation = self.residency_manager.validate_data_transfer(
            from_region="eu-west-1",
            to_region="eu-central-1",
            data_types=["analytics"]
        )
        
        assert "is_compliant" in validation
        
    def test_compliance_assessment_unregistered_system(self):
        """Test compliance assessment for unregistered system."""
        assessment = self.residency_manager.assess_residency_compliance("nonexistent_system")
        
        assert "error" in assessment
        assert assessment["score"] == 0
        
    def test_multiple_location_tracking(self):
        """Test tracking multiple data locations."""
        locations = [
            {
                "region": "eu-west-1",
                "country": "Ireland",
                "data_types": ["pii"],
                "storage_type": "primary"
            },
            {
                "region": "eu-central-1",
                "country": "Germany",
                "data_types": ["pii"],
                "storage_type": "backup"
            },
            {
                "region": "eu-west-2",
                "country": "UK",
                "data_types": ["analytics"],
                "storage_type": "archive"
            }
        ]
        
        for location in locations:
            self.residency_manager.track_data_location("test_system_1", location)
        
        # Run assessment to trigger location compliance check
        assessment = self.residency_manager.assess_residency_compliance("test_system_1")
        assert "score" in assessment
        
    def test_different_sovereignty_levels(self):
        """Test systems with different sovereignty levels."""
        # High sensitivity system
        self.residency_manager.register_system("high_sov_system", {
            "name": "High Sovereignty System",
            "jurisdictions": ["China"],
            "data_types": ["pii", "financial", "health"],
            "data_sensitivity": "critical",
            "sovereignty_requirements": "absolute"
        })
        
        # Low sensitivity system
        self.residency_manager.register_system("low_sov_system", {
            "name": "Low Sovereignty System",
            "jurisdictions": ["Global"],
            "data_types": ["public"],
            "data_sensitivity": "low"
        })
        
        high_assessment = self.residency_manager.assess_residency_compliance("high_sov_system")
        low_assessment = self.residency_manager.assess_residency_compliance("low_sov_system")
        
        assert "score" in high_assessment
        assert "score" in low_assessment
        
    def test_cross_border_transfer_validation(self):
        """Test cross-border data transfer validation."""
        # Register system with specific jurisdictions
        self.residency_manager.register_system("cross_border_system", {
            "name": "Cross Border System",
            "jurisdictions": ["EU", "US"],
            "data_types": ["pii", "financial"],
            "data_sensitivity": "high"
        })
        
        validation = self.residency_manager.validate_data_transfer(
            from_region="eu-west-1",
            to_region="us-east-1",
            data_types=["pii"],
            system_id="cross_border_system"
        )
        
        assert "is_compliant" in validation
        assert "requirements" in validation


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
