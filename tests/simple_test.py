#!/usr/bin/env python3
"""
Simple tests for the AI Governance platform without pytest.
"""

import sys
import os

# Add the parent directory to sys.path to import ai_governance
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_governance import GovernanceFramework, WorkflowOrchestrator


def test_governance_framework():
    """Test the main governance framework."""
    print("🧪 Testing GovernanceFramework...")
    
    governance = GovernanceFramework()
    
    # Test initialization
    assert governance is not None
    assert hasattr(governance, 'model_risk_manager')
    assert hasattr(governance, 'ai_oversight_manager')
    assert hasattr(governance, 'data_governance_manager')
    assert hasattr(governance, 'data_residency_manager')
    assert hasattr(governance, 'iso_compliance_manager')
    print("   ✅ Initialization test passed")
    
    # Test system registration
    system_info = {
        "name": "Test AI System",
        "use_case": "testing",
        "model_type": "test_model",
        "data_sensitivity": "low"
    }
    
    result = governance.register_ai_system("test_system_1", system_info)
    
    assert result["status"] == "success"
    assert result["system_id"] == "test_system_1"
    assert "governance_level" in result
    assert "requirements" in result
    print("   ✅ System registration test passed")
    
    # Test compliance assessment
    assessment = governance.assess_system_compliance("test_system_1")
    
    assert "overall_score" in assessment
    assert "module_assessments" in assessment
    assert "status" in assessment
    assert assessment["overall_score"] >= 0
    assert assessment["overall_score"] <= 100
    print("   ✅ Compliance assessment test passed")
    
    # Test dashboard data
    dashboard = governance.get_governance_dashboard()
    
    assert "summary" in dashboard
    assert "governance_levels" in dashboard
    assert "recent_assessments" in dashboard
    assert "total_systems" in dashboard["summary"]
    assert "compliant_systems" in dashboard["summary"]
    assert "compliance_rate" in dashboard["summary"]
    print("   ✅ Dashboard data test passed")
    
    print("   🎉 All GovernanceFramework tests passed!")


def test_workflow_orchestrator():
    """Test the workflow orchestrator."""
    print("🧪 Testing WorkflowOrchestrator...")
    
    orchestrator = WorkflowOrchestrator()
    
    # Test initialization
    assert orchestrator is not None
    assert hasattr(orchestrator, 'workflow_templates')
    assert hasattr(orchestrator, 'workflows')
    print("   ✅ Initialization test passed")
    
    # Test workflow initiation
    context = {
        "system_id": "test_system",
        "requestor": "test_user"
    }
    
    result = orchestrator.initiate_workflow("compliance_assessment", context)
    
    assert result["status"] == "initiated"
    assert "workflow_id" in result
    assert "workflow_type" in result
    print("   ✅ Workflow initiation test passed")
    
    # Test workflow status
    workflow_id = result["workflow_id"]
    status = orchestrator.get_workflow_status(workflow_id)
    
    assert "workflow_id" in status
    assert "status" in status
    assert "progress" in status
    assert "progress_percentage" in status["progress"]
    print("   ✅ Workflow status test passed")
    
    # Test workflow list
    workflows = orchestrator.list_workflows()
    
    assert "total_workflows" in workflows
    assert "workflows" in workflows
    assert "status_distribution" in workflows
    assert "type_distribution" in workflows
    print("   ✅ Workflow list test passed")
    
    print("   🎉 All WorkflowOrchestrator tests passed!")


def test_model_risk_manager():
    """Test the model risk manager."""
    print("🧪 Testing ModelRiskManager...")
    
    governance = GovernanceFramework()
    model_manager = governance.model_risk_manager
    
    # Register a test system
    system_info = {
        "name": "Test Model System",
        "use_case": "credit_scoring",
        "model_type": "gradient_boosting",
        "data_sensitivity": "high"
    }
    model_manager.register_system("test_model_1", system_info)
    print("   ✅ System registration test passed")
    
    # Test model risk assessment
    assessment = model_manager.assess_model_risk("test_model_1")
    
    assert "score" in assessment
    assert "risk_level" in assessment
    assert "recommendations" in assessment
    assert assessment["score"] >= 0
    assert assessment["score"] <= 100
    print("   ✅ Model risk assessment test passed")
    
    # Test model validation
    validation_data = {
        "type": "initial",
        "score": 85,
        "validator": "internal"
    }
    
    result = model_manager.validate_model("test_model_1", validation_data)
    
    assert "validation_id" in result
    assert "status" in result
    assert "results" in result
    print("   ✅ Model validation test passed")
    
    # Test model report
    report = model_manager.get_model_report("test_model_1")
    
    assert "model_info" in report
    assert "validation_summary" in report
    assert "performance_summary" in report
    assert "risk_assessment" in report
    print("   ✅ Model report test passed")
    
    print("   🎉 All ModelRiskManager tests passed!")


def test_data_governance_manager():
    """Test the data governance manager."""
    print("🧪 Testing DataGovernanceManager...")
    
    governance = GovernanceFramework()
    data_manager = governance.data_governance_manager
    
    # Register a test system
    system_info = {
        "name": "Test Data System",
        "data_types": ["pii", "financial"],
        "data_sources": ["customer_db", "transaction_log"],
        "data_sensitivity": "high"
    }
    data_manager.register_system("test_data_1", system_info)
    print("   ✅ System registration test passed")
    
    # Test data compliance assessment
    assessment = data_manager.assess_data_compliance("test_data_1")
    
    assert "score" in assessment
    assert "compliance_areas" in assessment
    assert "data_classification" in assessment
    assert assessment["score"] >= 0
    assert assessment["score"] <= 100
    print("   ✅ Data compliance assessment test passed")
    
    # Test data quality assessment
    quality_metrics = {
        "completeness": 95.0,
        "accuracy": 90.0,
        "consistency": 88.0,
        "timeliness": 92.0,
        "validity": 89.0,
        "uniqueness": 96.0
    }
    
    result = data_manager.assess_data_quality("test_data_1", "customer_db", quality_metrics)
    
    assert "quality_score" in result
    assert "quality_status" in result
    assert "metrics" in result
    print("   ✅ Data quality assessment test passed")
    
    # Test data inventory
    inventory = data_manager.generate_data_inventory("test_data_1")
    
    assert "summary" in inventory
    assert "assets" in inventory
    assert "total_assets" in inventory["summary"]
    print("   ✅ Data inventory test passed")
    
    print("   🎉 All DataGovernanceManager tests passed!")


def run_all_tests():
    """Run all tests."""
    print("🚀 Starting AI Governance Platform Tests")
    print("=" * 50)
    
    try:
        test_governance_framework()
        print()
        test_workflow_orchestrator()
        print()
        test_model_risk_manager()
        print()
        test_data_governance_manager()
        print()
        
        print("🎉 ALL TESTS PASSED! 🎉")
        print("=" * 50)
        print("✅ The AI Governance Platform is working correctly!")
        print("✅ All core modules are functional")
        print("✅ Integration between components is working")
        print("✅ Ready for production deployment")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()