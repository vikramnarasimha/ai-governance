#!/usr/bin/env python3
"""
Additional tests for Data Governance Manager to increase coverage.
"""

import pytest
import sys
import os

# Add the parent directory to sys.path to import ai_governance
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_governance.core.data_governance import DataGovernanceManager


class TestDataGovernanceManagerExtended:
    """Extended tests for Data Governance Manager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.data_manager = DataGovernanceManager()
        
        # Register test system
        self.data_manager.register_system("test_system_1", {
            "name": "Test Data System",
            "data_types": ["pii", "financial"],
            "data_sources": ["customer_db", "transaction_log"],
            "data_sensitivity": "high"
        })
        
    def test_privacy_compliance_check_gdpr(self):
        """Test GDPR privacy compliance check."""
        privacy_data = {
            "has_consent": True,
            "data_minimization": True,
            "right_to_erasure": True,
            "data_portability": True,
            "consent_management": True
        }
        
        result = self.data_manager.check_privacy_compliance("test_system_1", privacy_data)
        
        assert "overall_score" in result
        assert "compliance_status" in result
        assert "gdpr" in result["compliance_status"]
        
    def test_privacy_compliance_check_ccpa(self):
        """Test CCPA privacy compliance check."""
        privacy_data = {
            "opt_out_mechanism": True,
            "data_disclosure": True,
            "do_not_sell": True,
            "consumer_rights": True,
            "consent_management": True
        }
        
        result = self.data_manager.check_privacy_compliance("test_system_1", privacy_data)
        
        assert "overall_score" in result
        assert "compliance_status" in result
        
    def test_data_lineage_tracking(self):
        """Test data lineage tracking."""
        lineage_data = {
            "source": "customer_db",
            "transformations": [
                {"step": "anonymization", "tool": "data_anonymizer"},
                {"step": "aggregation", "tool": "data_processor"}
            ],
            "destination": "analytics_db",
            "timestamp": "2024-01-01T00:00:00"
        }
        
        self.data_manager.track_data_lineage("test_system_1", lineage_data)
        
        # Verify lineage was tracked
        assert "test_system_1" in self.data_manager.lineage_records
        
    def test_data_inventory_all_systems(self):
        """Test data inventory for all systems."""
        # Register multiple systems
        self.data_manager.register_system("test_system_2", {
            "name": "System 2",
            "data_types": ["analytics"],
            "data_sources": ["logs"]
        })
        
        inventory = self.data_manager.generate_data_inventory()
        
        assert "summary" in inventory
        assert "assets" in inventory
        assert "total_assets" in inventory["summary"]
        
    def test_data_quality_with_all_metrics(self):
        """Test data quality assessment with all metrics."""
        quality_metrics = {
            "completeness": 98.5,
            "accuracy": 96.0,
            "consistency": 94.0,
            "timeliness": 97.0,
            "validity": 95.5,
            "uniqueness": 99.0,
            "integrity": 93.0
        }
        
        result = self.data_manager.assess_data_quality("test_system_1", "customer_db", quality_metrics)
        
        assert "quality_score" in result
        assert "quality_status" in result
        assert result["quality_score"] >= 0
        
    def test_privacy_compliance_non_compliant(self):
        """Test privacy compliance with non-compliant data."""
        privacy_data = {
            "has_consent": False,
            "data_minimization": False,
            "consent_management": False
        }
        
        result = self.data_manager.check_privacy_compliance("test_system_1", privacy_data)
        
        assert "overall_score" in result
        # Should have lower score due to non-compliance
        
    def test_data_compliance_assessment_with_records(self):
        """Test data compliance assessment with existing records."""
        # First do a privacy compliance check
        privacy_data = {
            "has_consent": True,
            "data_minimization": True,
            "consent_management": True
        }
        self.data_manager.check_privacy_compliance("test_system_1", privacy_data)
        
        # Then assess overall compliance
        assessment = self.data_manager.assess_data_compliance("test_system_1")
        
        assert "score" in assessment
        assert assessment["score"] >= 0
        
    def test_data_lineage_multiple_entries(self):
        """Test tracking multiple lineage entries."""
        lineages = [
            {
                "source": "source_db_1",
                "transformations": [{"step": "transform_1"}],
                "destination": "dest_db_1"
            },
            {
                "source": "source_db_2",
                "transformations": [{"step": "transform_2"}],
                "destination": "dest_db_2"
            }
        ]
        
        for lineage in lineages:
            self.data_manager.track_data_lineage("test_system_1", lineage)
        
        assert len(self.data_manager.lineage_records.get("test_system_1", [])) >= 2
        
    def test_data_quality_poor_metrics(self):
        """Test data quality assessment with poor metrics."""
        quality_metrics = {
            "completeness": 50.0,
            "accuracy": 45.0,
            "consistency": 40.0,
            "timeliness": 55.0,
            "validity": 48.0,
            "uniqueness": 52.0
        }
        
        result = self.data_manager.assess_data_quality("test_system_1", "customer_db", quality_metrics)
        
        assert "quality_score" in result
        assert result["quality_score"] < 60  # Should be low
        
    def test_data_inventory_for_specific_system(self):
        """Test data inventory for specific system."""
        inventory = self.data_manager.generate_data_inventory("test_system_1")
        
        assert "summary" in inventory
        assert "assets" in inventory


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
