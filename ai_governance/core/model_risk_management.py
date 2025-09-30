"""
Model Risk Management module for AI governance.

Implements comprehensive model risk management practices for AI/ML models
in financial services, covering model validation, performance monitoring,
and risk assessment.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import json


class ModelRiskLevel(Enum):
    """Model risk levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ModelLifecycleStage(Enum):
    """Model lifecycle stages."""
    DEVELOPMENT = "development"
    VALIDATION = "validation"
    PRODUCTION = "production"
    MONITORING = "monitoring"
    RETIREMENT = "retirement"


class ModelRiskManager:
    """
    Manages model risk assessment and monitoring for AI systems.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize the model risk manager."""
        self.config = config or {}
        self.registered_models: Dict[str, Dict] = {}
        self.validation_history: Dict[str, List] = {}
        self.performance_metrics: Dict[str, List] = {}
        
    def register_system(self, system_id: str, system_info: Dict):
        """Register a system for model risk management."""
        model_record = {
            "system_id": system_id,
            "model_type": system_info.get("model_type", "unknown"),
            "use_case": system_info.get("use_case", ""),
            "risk_level": self._assess_model_risk_level(system_info),
            "lifecycle_stage": ModelLifecycleStage.DEVELOPMENT.value,
            "registered_at": datetime.utcnow().isoformat(),
            "validation_requirements": self._get_validation_requirements(system_info),
            "monitoring_requirements": self._get_monitoring_requirements(system_info)
        }
        
        self.registered_models[system_id] = model_record
        self.validation_history[system_id] = []
        self.performance_metrics[system_id] = []
    
    def assess_model_risk(self, system_id: str) -> Dict:
        """
        Assess model risk for a registered system.
        
        Args:
            system_id: System identifier
            
        Returns:
            Risk assessment results
        """
        if system_id not in self.registered_models:
            return {"error": "System not registered", "score": 0}
        
        model_record = self.registered_models[system_id]
        
        # Calculate risk score based on multiple factors
        risk_score = self._calculate_risk_score(system_id)
        
        # Check validation compliance
        validation_compliance = self._check_validation_compliance(system_id)
        
        # Check monitoring compliance
        monitoring_compliance = self._check_monitoring_compliance(system_id)
        
        # Overall compliance score
        overall_score = (risk_score + validation_compliance + monitoring_compliance) / 3
        
        assessment = {
            "system_id": system_id,
            "assessed_at": datetime.utcnow().isoformat(),
            "risk_level": model_record["risk_level"],
            "score": overall_score,
            "risk_score": risk_score,
            "validation_compliance": validation_compliance,
            "monitoring_compliance": monitoring_compliance,
            "recommendations": self._generate_recommendations(system_id, overall_score),
            "next_review_date": (datetime.utcnow() + timedelta(days=90)).isoformat()
        }
        
        return assessment
    
    def validate_model(self, system_id: str, validation_data: Dict) -> Dict:
        """
        Perform model validation.
        
        Args:
            system_id: System identifier
            validation_data: Validation test results and documentation
            
        Returns:
            Validation results
        """
        if system_id not in self.registered_models:
            return {"error": "System not registered"}
        
        # Mock validation process (in real implementation, this would involve
        # comprehensive statistical tests, bias analysis, etc.)
        validation_result = {
            "validation_id": f"val_{system_id}_{int(datetime.utcnow().timestamp())}",
            "system_id": system_id,
            "validated_at": datetime.utcnow().isoformat(),
            "validation_type": validation_data.get("type", "periodic"),
            "tests_performed": validation_data.get("tests", [
                "statistical_performance",
                "bias_analysis",
                "model_stability",
                "data_quality"
            ]),
            "results": {
                "overall_score": validation_data.get("score", 85),
                "performance_metrics": validation_data.get("performance", {}),
                "bias_metrics": validation_data.get("bias", {}),
                "stability_metrics": validation_data.get("stability", {})
            },
            "status": "passed" if validation_data.get("score", 85) >= 70 else "failed",
            "validator": validation_data.get("validator", "internal"),
            "comments": validation_data.get("comments", "")
        }
        
        # Store validation history
        self.validation_history[system_id].append(validation_result)
        
        # Update model lifecycle stage if appropriate
        if validation_result["status"] == "passed":
            self.registered_models[system_id]["lifecycle_stage"] = ModelLifecycleStage.PRODUCTION.value
        
        return validation_result
    
    def log_performance_metrics(self, system_id: str, metrics: Dict):
        """
        Log performance metrics for ongoing monitoring.
        
        Args:
            system_id: System identifier
            metrics: Performance metrics data
        """
        if system_id not in self.registered_models:
            return {"error": "System not registered"}
        
        metric_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": metrics,
            "alerts": self._check_performance_alerts(metrics)
        }
        
        self.performance_metrics[system_id].append(metric_entry)
        
        # Keep only last 1000 entries to prevent memory issues
        if len(self.performance_metrics[system_id]) > 1000:
            self.performance_metrics[system_id] = self.performance_metrics[system_id][-1000:]
    
    def get_model_report(self, system_id: str) -> Dict:
        """Generate comprehensive model risk report."""
        if system_id not in self.registered_models:
            return {"error": "System not registered"}
        
        model_record = self.registered_models[system_id]
        validation_history = self.validation_history.get(system_id, [])
        performance_history = self.performance_metrics.get(system_id, [])
        
        # Calculate trend analysis
        trend_analysis = self._analyze_performance_trends(performance_history)
        
        return {
            "model_info": model_record,
            "validation_summary": {
                "total_validations": len(validation_history),
                "last_validation": validation_history[-1] if validation_history else None,
                "validation_pass_rate": self._calculate_validation_pass_rate(validation_history)
            },
            "performance_summary": {
                "total_metrics": len(performance_history),
                "latest_metrics": performance_history[-1] if performance_history else None,
                "trend_analysis": trend_analysis,
                "alerts": self._get_recent_alerts(performance_history)
            },
            "risk_assessment": self.assess_model_risk(system_id)
        }
    
    def _assess_model_risk_level(self, system_info: Dict) -> str:
        """Assess the risk level of a model based on system information."""
        use_case = system_info.get("use_case", "").lower()
        model_type = system_info.get("model_type", "").lower()
        data_sensitivity = system_info.get("data_sensitivity", "medium").lower()
        
        risk_score = 0
        
        # High-risk use cases
        if any(case in use_case for case in ["credit", "fraud", "compliance", "pricing"]):
            risk_score += 3
        
        # Complex model types
        if any(model in model_type for model in ["neural", "deep", "ensemble"]):
            risk_score += 2
        
        # Data sensitivity
        if data_sensitivity == "high":
            risk_score += 2
        elif data_sensitivity == "medium":
            risk_score += 1
        
        if risk_score >= 5:
            return ModelRiskLevel.CRITICAL.value
        elif risk_score >= 3:
            return ModelRiskLevel.HIGH.value
        elif risk_score >= 1:
            return ModelRiskLevel.MEDIUM.value
        else:
            return ModelRiskLevel.LOW.value
    
    def _get_validation_requirements(self, system_info: Dict) -> List[str]:
        """Get validation requirements based on system information."""
        base_requirements = [
            "model_documentation",
            "performance_testing",
            "data_quality_validation"
        ]
        
        risk_level = self._assess_model_risk_level(system_info)
        
        if risk_level in [ModelRiskLevel.MEDIUM.value, ModelRiskLevel.HIGH.value, ModelRiskLevel.CRITICAL.value]:
            base_requirements.extend([
                "bias_testing",
                "stability_testing",
                "sensitivity_analysis"
            ])
        
        if risk_level in [ModelRiskLevel.HIGH.value, ModelRiskLevel.CRITICAL.value]:
            base_requirements.extend([
                "independent_validation",
                "stress_testing",
                "challenger_model_comparison"
            ])
        
        if risk_level == ModelRiskLevel.CRITICAL.value:
            base_requirements.extend([
                "regulatory_review",
                "board_approval",
                "continuous_validation"
            ])
        
        return base_requirements
    
    def _get_monitoring_requirements(self, system_info: Dict) -> List[str]:
        """Get monitoring requirements based on system information."""
        base_requirements = [
            "performance_tracking",
            "prediction_monitoring",
            "data_drift_detection"
        ]
        
        risk_level = self._assess_model_risk_level(system_info)
        
        if risk_level in [ModelRiskLevel.HIGH.value, ModelRiskLevel.CRITICAL.value]:
            base_requirements.extend([
                "real_time_monitoring",
                "automated_alerts",
                "escalation_procedures"
            ])
        
        return base_requirements
    
    def _calculate_risk_score(self, system_id: str) -> float:
        """Calculate risk score based on various factors."""
        # Mock implementation - would be more sophisticated in practice
        model_record = self.registered_models[system_id]
        risk_level = model_record["risk_level"]
        
        base_score = {
            ModelRiskLevel.LOW.value: 90,
            ModelRiskLevel.MEDIUM.value: 75,
            ModelRiskLevel.HIGH.value: 60,
            ModelRiskLevel.CRITICAL.value: 45
        }.get(risk_level, 50)
        
        # Adjust based on lifecycle stage
        stage = model_record.get("lifecycle_stage", ModelLifecycleStage.DEVELOPMENT.value)
        if stage == ModelLifecycleStage.PRODUCTION.value:
            base_score += 10
        elif stage == ModelLifecycleStage.VALIDATION.value:
            base_score += 5
        
        return min(100, base_score)
    
    def _check_validation_compliance(self, system_id: str) -> float:
        """Check validation compliance for a system."""
        validation_history = self.validation_history.get(system_id, [])
        
        if not validation_history:
            return 0  # No validation performed
        
        # Check if recent validation exists (within 6 months)
        recent_validations = [
            v for v in validation_history
            if (datetime.utcnow() - datetime.fromisoformat(v["validated_at"])).days <= 180
        ]
        
        if not recent_validations:
            return 30  # Outdated validation
        
        # Calculate pass rate
        passed_validations = [v for v in recent_validations if v["status"] == "passed"]
        pass_rate = len(passed_validations) / len(recent_validations)
        
        return pass_rate * 100
    
    def _check_monitoring_compliance(self, system_id: str) -> float:
        """Check monitoring compliance for a system."""
        performance_history = self.performance_metrics.get(system_id, [])
        
        if not performance_history:
            return 0  # No monitoring data
        
        # Check if recent metrics exist (within 7 days)
        recent_metrics = [
            m for m in performance_history
            if (datetime.utcnow() - datetime.fromisoformat(m["timestamp"])).days <= 7
        ]
        
        if not recent_metrics:
            return 40  # Outdated monitoring
        
        # Check for alerts
        recent_alerts = sum(1 for m in recent_metrics if m.get("alerts"))
        alert_rate = recent_alerts / len(recent_metrics) if recent_metrics else 0
        
        # Lower alert rate = better compliance
        return max(50, 100 - (alert_rate * 50))
    
    def _generate_recommendations(self, system_id: str, score: float) -> List[str]:
        """Generate recommendations based on assessment score."""
        recommendations = []
        
        if score < 70:
            recommendations.append("Immediate review required - compliance below threshold")
        
        if score < 50:
            recommendations.append("Consider suspending model until compliance improves")
        
        # Add specific recommendations based on validation and monitoring
        validation_history = self.validation_history.get(system_id, [])
        if not validation_history:
            recommendations.append("Perform initial model validation")
        elif len(validation_history) == 0 or (datetime.utcnow() - 
                datetime.fromisoformat(validation_history[-1]["validated_at"])).days > 180:
            recommendations.append("Update model validation - last validation is outdated")
        
        performance_history = self.performance_metrics.get(system_id, [])
        if not performance_history:
            recommendations.append("Implement performance monitoring")
        elif (datetime.utcnow() - 
              datetime.fromisoformat(performance_history[-1]["timestamp"])).days > 7:
            recommendations.append("Update performance monitoring - data is stale")
        
        return recommendations
    
    def _analyze_performance_trends(self, performance_history: List) -> Dict:
        """Analyze performance trends over time."""
        if len(performance_history) < 2:
            return {"trend": "insufficient_data"}
        
        # Simple trend analysis based on recent vs older metrics
        recent_metrics = performance_history[-10:]  # Last 10 entries
        older_metrics = performance_history[-20:-10] if len(performance_history) >= 20 else []
        
        if not older_metrics:
            return {"trend": "insufficient_historical_data"}
        
        # Mock trend calculation (would be more sophisticated in practice)
        recent_avg = sum(m.get("metrics", {}).get("accuracy", 0) for m in recent_metrics) / len(recent_metrics)
        older_avg = sum(m.get("metrics", {}).get("accuracy", 0) for m in older_metrics) / len(older_metrics)
        
        if recent_avg > older_avg + 0.05:
            trend = "improving"
        elif recent_avg < older_avg - 0.05:
            trend = "degrading"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "recent_average": recent_avg,
            "historical_average": older_avg
        }
    
    def _calculate_validation_pass_rate(self, validation_history: List) -> float:
        """Calculate the pass rate for validations."""
        if not validation_history:
            return 0
        
        passed = sum(1 for v in validation_history if v["status"] == "passed")
        return (passed / len(validation_history)) * 100
    
    def _get_recent_alerts(self, performance_history: List) -> List:
        """Get recent performance alerts."""
        recent_history = performance_history[-30:]  # Last 30 entries
        alerts = []
        
        for entry in recent_history:
            if entry.get("alerts"):
                alerts.extend(entry["alerts"])
        
        return alerts[-10:]  # Return last 10 alerts
    
    def _check_performance_alerts(self, metrics: Dict) -> List[str]:
        """Check if performance metrics trigger any alerts."""
        alerts = []
        
        # Example alert conditions
        accuracy = metrics.get("accuracy", 1.0)
        if accuracy < 0.8:
            alerts.append(f"Low accuracy detected: {accuracy:.2f}")
        
        precision = metrics.get("precision", 1.0)
        if precision < 0.7:
            alerts.append(f"Low precision detected: {precision:.2f}")
        
        data_drift = metrics.get("data_drift_score", 0.0)
        if data_drift > 0.3:
            alerts.append(f"High data drift detected: {data_drift:.2f}")
        
        return alerts