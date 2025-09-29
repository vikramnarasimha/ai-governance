#!/usr/bin/env python3
"""
Basic tests for the AI Governance platform.
Run with: python -m pytest tests/ -v
"""

import pytest
import sys
import os

# Add the parent directory to sys.path to import ai_governance
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_governance import GovernanceFramework, WorkflowOrchestrator


class TestGovernanceFramework:
    """Test the main governance framework."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.governance = GovernanceFramework()
        
    def test_initialization(self):
        """Test framework initialization."""
        assert self.governance is not None
        assert hasattr(self.governance, 'model_risk_manager')
        assert hasattr(self.governance, 'ai_oversight_manager')
        assert hasattr(self.governance, 'data_governance_manager')
        assert hasattr(self.governance, 'data_residency_manager')
        assert hasattr(self.governance, 'iso_compliance_manager')
        
    def test_system_registration(self):
        """Test AI system registration."""
        system_info = {
            "name": "Test AI System",
            "use_case": "testing",
            "model_type": "test_model",
            "data_sensitivity": "low"
        }
        
        result = self.governance.register_ai_system("test_system_1", system_info)
        
        assert result["status"] == "success"
        assert result["system_id"] == "test_system_1"
        assert "governance_level" in result
        assert "requirements" in result
        
    def test_compliance_assessment(self):
        """Test compliance assessment."""
        # First register a system
        system_info = {
            "name": "Test AI System",
            "use_case": "testing",
            "model_type": "test_model",
            "data_sensitivity": "medium"
        }
        
        self.governance.register_ai_system("test_system_2", system_info)
        
        # Then assess compliance
        assessment = self.governance.assess_system_compliance("test_system_2")
        
        assert "overall_score" in assessment
        assert "module_assessments" in assessment
        assert "status" in assessment
        assert assessment["overall_score"] >= 0
        assert assessment["overall_score"] <= 100
        
    def test_dashboard_data(self):
        """Test dashboard data generation."""
        dashboard = self.governance.get_governance_dashboard()
        
        assert "summary" in dashboard
        assert "governance_levels" in dashboard
        assert "recent_assessments" in dashboard
        assert "total_systems" in dashboard["summary"]
        assert "compliant_systems" in dashboard["summary"]
        assert "compliance_rate" in dashboard["summary"]


class TestWorkflowOrchestrator:
    """Test the workflow orchestrator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.orchestrator = WorkflowOrchestrator()
        
    def test_initialization(self):
        """Test orchestrator initialization."""
        assert self.orchestrator is not None
        assert hasattr(self.orchestrator, 'workflow_templates')
        assert hasattr(self.orchestrator, 'workflows')
        
    def test_workflow_initiation(self):
        """Test workflow initiation."""
        context = {
            "system_id": "test_system",
            "requestor": "test_user"
        }
        
        result = self.orchestrator.initiate_workflow("compliance_assessment", context)
        
        assert result["status"] == "initiated"
        assert "workflow_id" in result
        assert "workflow_type" in result
        
    def test_workflow_status(self):
        """Test workflow status retrieval."""
        # First initiate a workflow
        context = {"system_id": "test_system"}
        result = self.orchestrator.initiate_workflow("compliance_assessment", context)
        workflow_id = result["workflow_id"]
        
        # Then get status
        status = self.orchestrator.get_workflow_status(workflow_id)
        
        assert "workflow_id" in status
        assert "status" in status
        assert "progress" in status
        assert "progress_percentage" in status["progress"]
        
    def test_workflow_list(self):
        """Test workflow listing."""
        workflows = self.orchestrator.list_workflows()
        
        assert "total_workflows" in workflows
        assert "workflows" in workflows
        assert "status_distribution" in workflows
        assert "type_distribution" in workflows


class TestModelRiskManager:
    """Test the model risk manager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.governance = GovernanceFramework()
        self.model_manager = self.governance.model_risk_manager
        
        # Register a test system
        system_info = {
            "name": "Test Model System",
            "use_case": "credit_scoring",
            "model_type": "gradient_boosting",
            "data_sensitivity": "high"
        }
        self.model_manager.register_system("test_model_1", system_info)
        
    def test_model_risk_assessment(self):
        """Test model risk assessment."""
        assessment = self.model_manager.assess_model_risk("test_model_1")
        
        assert "score" in assessment
        assert "risk_level" in assessment
        assert "recommendations" in assessment
        assert assessment["score"] >= 0
        assert assessment["score"] <= 100
        
    def test_model_validation(self):
        """Test model validation."""
        validation_data = {
            "type": "initial",
            "score": 85,
            "validator": "internal"
        }
        
        result = self.model_manager.validate_model("test_model_1", validation_data)
        
        assert "validation_id" in result
        assert "status" in result
        assert "results" in result
        
    def test_model_report(self):
        """Test model report generation."""
        report = self.model_manager.get_model_report("test_model_1")
        
        assert "model_info" in report
        assert "validation_summary" in report
        assert "performance_summary" in report
        assert "risk_assessment" in report


class TestDataGovernanceManager:
    """Test the data governance manager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.governance = GovernanceFramework()
        self.data_manager = self.governance.data_governance_manager
        
        # Register a test system
        system_info = {
            "name": "Test Data System",
            "data_types": ["pii", "financial"],
            "data_sources": ["customer_db", "transaction_log"],
            "data_sensitivity": "high"
        }
        self.data_manager.register_system("test_data_1", system_info)
        
    def test_data_compliance_assessment(self):
        """Test data governance compliance assessment."""
        assessment = self.data_manager.assess_data_compliance("test_data_1")
        
        assert "score" in assessment
        assert "compliance_areas" in assessment
        assert "data_classification" in assessment
        assert assessment["score"] >= 0
        assert assessment["score"] <= 100
        
    def test_data_quality_assessment(self):
        """Test data quality assessment."""
        quality_metrics = {
            "completeness": 95.0,
            "accuracy": 90.0,
            "consistency": 88.0,
            "timeliness": 92.0,
            "validity": 89.0,
            "uniqueness": 96.0
        }
        
        result = self.data_manager.assess_data_quality("test_data_1", "customer_db", quality_metrics)
        
        assert "quality_score" in result
        assert "quality_status" in result
        assert "metrics" in result
        
    def test_data_inventory(self):
        """Test data inventory generation."""
        inventory = self.data_manager.generate_data_inventory("test_data_1")
        
        assert "summary" in inventory
        assert "assets" in inventory
        assert "total_assets" in inventory["summary"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])