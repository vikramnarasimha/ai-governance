#!/usr/bin/env python3
"""
Example script demonstrating the AI Governance platform capabilities.
This script shows how to register AI systems, run assessments, and manage workflows.
"""

import sys
import json
from datetime import datetime

# Add the parent directory to sys.path to import ai_governance
sys.path.append('.')

from ai_governance import GovernanceFramework, WorkflowOrchestrator


def main():
    """Demonstrate AI governance platform capabilities."""
    print("🤖 AI Governance Platform Demo")
    print("=" * 50)
    
    # Initialize the governance framework
    config = {
        "model_risk": {"validation_threshold": 80},
        "ai_oversight": {"monitoring_frequency": "daily"},
        "data_governance": {"quality_threshold": 85},
        "data_residency": {"default_region": "us-east-1"},
        "iso_compliance": {"target_maturity": "managed"}
    }
    
    governance = GovernanceFramework(config)
    orchestrator = WorkflowOrchestrator()
    
    print(f"✅ Initialized governance framework at {governance.created_at}")
    print()
    
    # Example 1: Register a credit scoring AI system
    print("📋 Example 1: Registering Credit Scoring AI System")
    print("-" * 50)
    
    credit_system_info = {
        "name": "Credit Risk Assessment Model",
        "description": "AI model for credit risk assessment and loan approval decisions",
        "use_case": "credit_scoring",
        "model_type": "gradient_boosting",
        "data_sources": ["customer_data", "credit_bureau", "transaction_history"],
        "data_types": ["pii", "financial", "behavioral"],
        "data_sensitivity": "high",
        "risk_factors": ["regulatory_compliance", "bias_risk", "model_complexity"],
        "jurisdictions": ["us", "eu"],
        "cloud_provider": "aws",
        "industry_sector": "financial_services",
        "regulatory_scope": ["basel", "gdpr", "ccpa"]
    }
    
    registration_result = governance.register_ai_system("credit_model_v1", credit_system_info)
    print(f"✅ System registered: {registration_result['system_id']}")
    print(f"   Governance Level: {registration_result['governance_level']}")
    print(f"   Requirements: {len(registration_result['requirements'])} items")
    print()
    
    # Example 2: Register a fraud detection system
    print("📋 Example 2: Registering Fraud Detection AI System")
    print("-" * 50)
    
    fraud_system_info = {
        "name": "Real-time Fraud Detection",
        "description": "AI system for detecting fraudulent transactions in real-time",
        "use_case": "fraud_detection",
        "model_type": "neural_network",
        "data_sources": ["transaction_data", "device_data", "user_behavior"],
        "data_types": ["pii", "financial", "behavioral"],
        "data_sensitivity": "high",
        "risk_factors": ["real_time_decisions", "false_positives", "regulatory_compliance"],
        "jurisdictions": ["us"],
        "cloud_provider": "aws",
        "industry_sector": "financial_services"
    }
    
    registration_result2 = governance.register_ai_system("fraud_detector_v2", fraud_system_info)
    print(f"✅ System registered: {registration_result2['system_id']}")
    print(f"   Governance Level: {registration_result2['governance_level']}")
    print()
    
    # Example 3: Run compliance assessments
    print("🔍 Example 3: Running Compliance Assessments")
    print("-" * 50)
    
    # Assess credit scoring system
    credit_assessment = governance.assess_system_compliance("credit_model_v1")
    print(f"Credit Model Assessment:")
    print(f"   Overall Score: {credit_assessment['overall_score']:.1f}/100")
    print(f"   Status: {credit_assessment['status']}")
    print(f"   Module Scores:")
    for module, result in credit_assessment['module_assessments'].items():
        score = result.get('score', 0)
        print(f"     - {module}: {score:.1f}/100")
    print()
    
    # Assess fraud detection system
    fraud_assessment = governance.assess_system_compliance("fraud_detector_v2")
    print(f"Fraud Detection Assessment:")
    print(f"   Overall Score: {fraud_assessment['overall_score']:.1f}/100")
    print(f"   Status: {fraud_assessment['status']}")
    print()
    
    # Example 4: Model validation workflow
    print("⚙️ Example 4: Model Validation Workflow")
    print("-" * 50)
    
    # Perform model validation for credit system
    validation_data = {
        "type": "comprehensive",
        "score": 87,
        "tests": [
            "statistical_performance",
            "bias_analysis",
            "model_stability",
            "data_quality",
            "challenger_model_comparison"
        ],
        "performance": {
            "accuracy": 0.89,
            "precision": 0.86,
            "recall": 0.91,
            "f1_score": 0.88
        },
        "bias": {
            "demographic_parity": 0.95,
            "equalized_odds": 0.93,
            "calibration": 0.96
        },
        "validator": "third_party",
        "comments": "Model passes all validation tests with good performance metrics"
    }
    
    validation_result = governance.model_risk_manager.validate_model("credit_model_v1", validation_data)
    print(f"✅ Model validation completed: {validation_result['validation_id']}")
    print(f"   Status: {validation_result['status']}")
    print(f"   Overall Score: {validation_result['results']['overall_score']}")
    print()
    
    # Example 5: Data quality assessment
    print("📊 Example 5: Data Quality Assessment")
    print("-" * 50)
    
    quality_metrics = {
        "completeness": 94.5,
        "accuracy": 91.2,
        "consistency": 88.7,
        "timeliness": 96.1,
        "validity": 89.3,
        "uniqueness": 97.8
    }
    
    quality_result = governance.data_governance_manager.assess_data_quality(
        "credit_model_v1", "customer_data", quality_metrics
    )
    print(f"✅ Data quality assessment completed")
    print(f"   Overall Quality Score: {quality_result['quality_score']:.1f}/100")
    print(f"   Quality Status: {quality_result['quality_status']}")
    if quality_result['issues']:
        print(f"   Issues Identified: {len(quality_result['issues'])}")
        for issue in quality_result['issues']:
            print(f"     - {issue}")
    print()
    
    # Example 6: Data residency tracking
    print("🌍 Example 6: Data Residency Tracking")
    print("-" * 50)
    
    location_data = {
        "data_stores": [
            {"type": "primary", "region": "us-east-1", "service": "rds"},
            {"type": "backup", "region": "us-west-2", "service": "s3"}
        ],
        "processing_locations": [
            {"region": "us-east-1", "service": "ec2"}
        ],
        "backup_locations": [
            {"region": "us-west-2", "service": "s3"}
        ],
        "transit_paths": []
    }
    
    residency_result = governance.data_residency_manager.track_data_location("credit_model_v1", location_data)
    print(f"✅ Data location tracked: {residency_result['status']}")
    if residency_result['violations']:
        print(f"   ⚠️ Violations detected: {len(residency_result['violations'])}")
    else:
        print(f"   ✅ No violations detected")
    print()
    
    # Example 7: Workflow orchestration
    print("⚙️ Example 7: Workflow Orchestration")
    print("-" * 50)
    
    # Initiate compliance assessment workflow
    workflow_context = {
        "system_id": "credit_model_v1",
        "assessment_type": "comprehensive",
        "requestor": "risk_manager"
    }
    
    workflow_result = orchestrator.initiate_workflow("compliance_assessment", workflow_context)
    workflow_id = workflow_result['workflow_id']
    print(f"✅ Workflow initiated: {workflow_id}")
    print(f"   Type: {workflow_result['workflow_type']}")
    
    # Check workflow status
    status = orchestrator.get_workflow_status(workflow_id)
    print(f"   Status: {status['status']}")
    print(f"   Progress: {status['progress']['progress_percentage']:.1f}%")
    print()
    
    # Example 8: Generate governance dashboard
    print("📊 Example 8: Governance Dashboard")
    print("-" * 50)
    
    dashboard = governance.get_governance_dashboard()
    print(f"Dashboard Summary:")
    print(f"   Total Systems: {dashboard['summary']['total_systems']}")
    print(f"   Compliant Systems: {dashboard['summary']['compliant_systems']}")
    print(f"   Compliance Rate: {dashboard['summary']['compliance_rate']:.1f}%")
    print(f"   Governance Level Distribution:")
    for level, count in dashboard['governance_levels'].items():
        print(f"     - {level}: {count}")
    print()
    
    # Example 9: ISO compliance assessment
    print("📋 Example 9: ISO Compliance Assessment")
    print("-" * 50)
    
    iso_assessment = governance.iso_compliance_manager.assess_iso_compliance("credit_model_v1")
    print(f"ISO Compliance Assessment:")
    print(f"   Overall Score: {iso_assessment['score']:.1f}/100")
    print(f"   Maturity Level: {iso_assessment['maturity_level']}")
    print(f"   Target Maturity: {iso_assessment['target_maturity_level']}")
    print(f"   Applicable Standards: {', '.join(iso_assessment['applicable_standards'])}")
    if iso_assessment['gaps_identified']:
        print(f"   Gaps Identified: {len(iso_assessment['gaps_identified'])}")
    print()
    
    # Example 10: Generate comprehensive report
    print("📄 Example 10: Comprehensive Governance Report")
    print("-" * 50)
    
    model_report = governance.model_risk_manager.get_model_report("credit_model_v1")
    print(f"Model Risk Report for {model_report['model_info']['system_id']}:")
    print(f"   Risk Level: {model_report['model_info']['risk_level']}")
    print(f"   Lifecycle Stage: {model_report['model_info']['lifecycle_stage']}")
    print(f"   Total Validations: {model_report['validation_summary']['total_validations']}")
    print(f"   Validation Pass Rate: {model_report['validation_summary']['validation_pass_rate']:.1f}%")
    
    if model_report['performance_summary']['latest_metrics']:
        latest_metrics = model_report['performance_summary']['latest_metrics']
        print(f"   Latest Performance:")
        metrics = latest_metrics.get('metrics', {})
        for metric, value in metrics.items():
            print(f"     - {metric}: {value}")
    print()
    
    # Summary
    print("🎉 Demo Complete!")
    print("=" * 50)
    print("This demo showed:")
    print("✅ System registration with governance level assignment")
    print("✅ Comprehensive compliance assessments across all modules")
    print("✅ Model validation and performance tracking")
    print("✅ Data quality monitoring and assessment")
    print("✅ Data residency compliance tracking")
    print("✅ Workflow orchestration and automation")
    print("✅ ISO standards compliance assessment")
    print("✅ Dashboard and reporting capabilities")
    print()
    print("🚀 The AI Governance Platform is ready for production use!")
    print("   Visit http://localhost:8000 to access the web interface")
    print("   Visit http://localhost:8000/api/docs for API documentation")


if __name__ == "__main__":
    main()