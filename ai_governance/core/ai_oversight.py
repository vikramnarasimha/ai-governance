"""
AI Oversight module for comprehensive AI system governance.

Implements oversight mechanisms for AI systems including monitoring,
audit trails, decision transparency, and regulatory compliance.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import json


class OversightLevel(Enum):
    """AI oversight levels."""
    BASIC = "basic"
    ENHANCED = "enhanced"
    COMPREHENSIVE = "comprehensive"


class DecisionType(Enum):
    """Types of AI decisions requiring oversight."""
    AUTOMATED = "automated"
    HUMAN_IN_LOOP = "human_in_loop"
    HUMAN_APPROVAL = "human_approval"


class AIOversightManager:
    """
    Manages AI oversight including monitoring, audit trails, and transparency.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize the AI oversight manager."""
        self.config = config or {}
        self.registered_systems: Dict[str, Dict] = {}
        self.audit_trails: Dict[str, List] = {}
        self.decision_logs: Dict[str, List] = {}
        self.oversight_reports: Dict[str, List] = {}
        
    def register_system(self, system_id: str, system_info: Dict):
        """Register a system for AI oversight."""
        oversight_record = {
            "system_id": system_id,
            "system_name": system_info.get("name", system_id),
            "oversight_level": self._determine_oversight_level(system_info),
            "decision_type": self._determine_decision_type(system_info),
            "registered_at": datetime.utcnow().isoformat(),
            "oversight_requirements": self._get_oversight_requirements(system_info),
            "monitoring_config": self._get_monitoring_config(system_info),
            "escalation_rules": self._get_escalation_rules(system_info)
        }
        
        self.registered_systems[system_id] = oversight_record
        self.audit_trails[system_id] = []
        self.decision_logs[system_id] = []
        self.oversight_reports[system_id] = []
        
        # Log registration
        self._log_audit_event(system_id, "system_registered", {
            "oversight_level": oversight_record["oversight_level"],
            "decision_type": oversight_record["decision_type"]
        })
    
    def assess_oversight_compliance(self, system_id: str) -> Dict:
        """
        Assess oversight compliance for a registered system.
        
        Args:
            system_id: System identifier
            
        Returns:
            Oversight compliance assessment
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered", "score": 0}
        
        system_record = self.registered_systems[system_id]
        
        # Check various compliance aspects
        monitoring_compliance = self._check_monitoring_compliance(system_id)
        audit_compliance = self._check_audit_compliance(system_id)
        transparency_compliance = self._check_transparency_compliance(system_id)
        escalation_compliance = self._check_escalation_compliance(system_id)
        
        # Calculate overall compliance score
        overall_score = (
            monitoring_compliance * 0.3 +
            audit_compliance * 0.25 +
            transparency_compliance * 0.25 +
            escalation_compliance * 0.2
        )
        
        assessment = {
            "system_id": system_id,
            "assessed_at": datetime.utcnow().isoformat(),
            "oversight_level": system_record["oversight_level"],
            "score": overall_score,
            "compliance_areas": {
                "monitoring": monitoring_compliance,
                "audit_trail": audit_compliance,
                "transparency": transparency_compliance,
                "escalation": escalation_compliance
            },
            "recommendations": self._generate_oversight_recommendations(system_id, overall_score),
            "next_review_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
        }
        
        # Log assessment
        self._log_audit_event(system_id, "compliance_assessment", {
            "score": overall_score,
            "assessment_id": assessment.get("assessment_id", "unknown")
        })
        
        return assessment
    
    def log_decision(self, system_id: str, decision_data: Dict):
        """
        Log an AI decision for audit and oversight.
        
        Args:
            system_id: System identifier
            decision_data: Decision details including inputs, outputs, and context
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered"}
        
        decision_log = {
            "decision_id": decision_data.get("decision_id", f"dec_{int(datetime.utcnow().timestamp())}"),
            "system_id": system_id,
            "timestamp": datetime.utcnow().isoformat(),
            "decision_type": decision_data.get("type", "automated"),
            "inputs": decision_data.get("inputs", {}),
            "outputs": decision_data.get("outputs", {}),
            "confidence": decision_data.get("confidence", None),
            "human_reviewer": decision_data.get("human_reviewer", None),
            "context": decision_data.get("context", {}),
            "explanation": decision_data.get("explanation", ""),
            "risk_level": decision_data.get("risk_level", "medium")
        }
        
        self.decision_logs[system_id].append(decision_log)
        
        # Check if escalation is needed
        self._check_decision_escalation(system_id, decision_log)
        
        # Keep only last 10000 decisions to prevent memory issues
        if len(self.decision_logs[system_id]) > 10000:
            self.decision_logs[system_id] = self.decision_logs[system_id][-10000:]
        
        return {"status": "logged", "decision_id": decision_log["decision_id"]}
    
    def generate_transparency_report(self, system_id: str, start_date: str = None, end_date: str = None) -> Dict:
        """
        Generate transparency report for AI system decisions.
        
        Args:
            system_id: System identifier
            start_date: Start date for report (ISO format)
            end_date: End date for report (ISO format)
            
        Returns:
            Transparency report with decision analytics
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered"}
        
        # Filter decisions by date range
        decisions = self._filter_decisions_by_date(system_id, start_date, end_date)
        
        if not decisions:
            return {"error": "No decisions found for the specified period"}
        
        # Analyze decisions
        decision_analytics = self._analyze_decisions(decisions)
        
        report = {
            "system_id": system_id,
            "report_generated_at": datetime.utcnow().isoformat(),
            "period": {
                "start_date": start_date or decisions[0]["timestamp"],
                "end_date": end_date or decisions[-1]["timestamp"]
            },
            "summary": {
                "total_decisions": len(decisions),
                "decision_types": decision_analytics["decision_types"],
                "risk_distribution": decision_analytics["risk_distribution"],
                "confidence_stats": decision_analytics["confidence_stats"]
            },
            "compliance_metrics": {
                "human_oversight_rate": decision_analytics["human_oversight_rate"],
                "explanation_coverage": decision_analytics["explanation_coverage"],
                "escalation_rate": decision_analytics["escalation_rate"]
            },
            "recommendations": self._generate_transparency_recommendations(decision_analytics)
        }
        
        # Store report
        self.oversight_reports[system_id].append(report)
        
        return report
    
    def get_audit_trail(self, system_id: str, event_type: str = None, limit: int = 100) -> Dict:
        """
        Retrieve audit trail for a system.
        
        Args:
            system_id: System identifier
            event_type: Filter by event type (optional)
            limit: Maximum number of events to return
            
        Returns:
            Audit trail events
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered"}
        
        audit_events = self.audit_trails.get(system_id, [])
        
        # Filter by event type if specified
        if event_type:
            audit_events = [e for e in audit_events if e.get("event_type") == event_type]
        
        # Apply limit
        audit_events = audit_events[-limit:] if limit else audit_events
        
        return {
            "system_id": system_id,
            "total_events": len(self.audit_trails.get(system_id, [])),
            "filtered_events": len(audit_events),
            "events": audit_events
        }
    
    def escalate_decision(self, system_id: str, decision_id: str, escalation_reason: str, escalated_by: str):
        """
        Escalate a decision for human review.
        
        Args:
            system_id: System identifier
            decision_id: Decision identifier
            escalation_reason: Reason for escalation
            escalated_by: Person or system escalating
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered"}
        
        # Find the decision
        decisions = self.decision_logs.get(system_id, [])
        decision = next((d for d in decisions if d["decision_id"] == decision_id), None)
        
        if not decision:
            return {"error": "Decision not found"}
        
        escalation_data = {
            "escalation_id": f"esc_{int(datetime.utcnow().timestamp())}",
            "decision_id": decision_id,
            "escalated_at": datetime.utcnow().isoformat(),
            "escalation_reason": escalation_reason,
            "escalated_by": escalated_by,
            "status": "pending_review",
            "original_decision": decision
        }
        
        # Log escalation
        self._log_audit_event(system_id, "decision_escalated", escalation_data)
        
        return {"status": "escalated", "escalation_id": escalation_data["escalation_id"]}
    
    def _determine_oversight_level(self, system_info: Dict) -> str:
        """Determine the required oversight level for a system."""
        use_case = system_info.get("use_case", "").lower()
        risk_level = system_info.get("risk_level", "medium").lower()
        regulatory_scope = system_info.get("regulatory_scope", [])
        
        # High-risk use cases require comprehensive oversight
        if any(case in use_case for case in ["credit", "compliance", "fraud", "regulatory"]):
            return OversightLevel.COMPREHENSIVE.value
        
        # Systems under regulatory scrutiny
        if regulatory_scope:
            return OversightLevel.COMPREHENSIVE.value
        
        # High risk level systems
        if risk_level in ["high", "critical"]:
            return OversightLevel.ENHANCED.value
        
        return OversightLevel.BASIC.value
    
    def _determine_decision_type(self, system_info: Dict) -> str:
        """Determine the decision type for a system."""
        automation_level = system_info.get("automation_level", "automated").lower()
        use_case = system_info.get("use_case", "").lower()
        
        # Critical decisions require human approval
        if any(case in use_case for case in ["credit_approval", "compliance_violation"]):
            return DecisionType.HUMAN_APPROVAL.value
        
        # High-risk decisions need human in the loop
        if automation_level == "human_in_loop" or "high_risk" in use_case:
            return DecisionType.HUMAN_IN_LOOP.value
        
        return DecisionType.AUTOMATED.value
    
    def _get_oversight_requirements(self, system_info: Dict) -> List[str]:
        """Get oversight requirements based on system information."""
        oversight_level = self._determine_oversight_level(system_info)
        
        base_requirements = [
            "decision_logging",
            "basic_monitoring",
            "audit_trail"
        ]
        
        if oversight_level in [OversightLevel.ENHANCED.value, OversightLevel.COMPREHENSIVE.value]:
            base_requirements.extend([
                "detailed_explanations",
                "performance_monitoring",
                "bias_monitoring"
            ])
        
        if oversight_level == OversightLevel.COMPREHENSIVE.value:
            base_requirements.extend([
                "real_time_monitoring",
                "human_oversight",
                "regulatory_reporting",
                "escalation_procedures"
            ])
        
        return base_requirements
    
    def _get_monitoring_config(self, system_info: Dict) -> Dict:
        """Get monitoring configuration based on system information."""
        oversight_level = self._determine_oversight_level(system_info)
        
        config = {
            "frequency": "daily",
            "metrics": ["accuracy", "throughput", "response_time"],
            "alerts": ["performance_degradation", "high_error_rate"]
        }
        
        if oversight_level in [OversightLevel.ENHANCED.value, OversightLevel.COMPREHENSIVE.value]:
            config.update({
                "frequency": "hourly",
                "metrics": config["metrics"] + ["bias_metrics", "fairness_indicators"],
                "alerts": config["alerts"] + ["bias_alert", "fairness_violation"]
            })
        
        if oversight_level == OversightLevel.COMPREHENSIVE.value:
            config.update({
                "frequency": "real_time",
                "alerts": config["alerts"] + ["regulatory_threshold_breach", "compliance_violation"]
            })
        
        return config
    
    def _get_escalation_rules(self, system_info: Dict) -> List[Dict]:
        """Get escalation rules based on system information."""
        rules = [
            {
                "condition": "confidence < 0.7",
                "action": "flag_for_review",
                "severity": "medium"
            },
            {
                "condition": "error_rate > 0.1",
                "action": "immediate_review",
                "severity": "high"
            }
        ]
        
        oversight_level = self._determine_oversight_level(system_info)
        
        if oversight_level == OversightLevel.COMPREHENSIVE.value:
            rules.extend([
                {
                    "condition": "bias_score > 0.2",
                    "action": "suspend_system",
                    "severity": "critical"
                },
                {
                    "condition": "regulatory_threshold_breach",
                    "action": "immediate_escalation",
                    "severity": "critical"
                }
            ])
        
        return rules
    
    def _log_audit_event(self, system_id: str, event_type: str, event_data: Dict):
        """Log an audit event for a system."""
        audit_event = {
            "event_id": f"audit_{int(datetime.utcnow().timestamp())}",
            "system_id": system_id,
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "event_data": event_data,
            "source": "ai_oversight_manager"
        }
        
        self.audit_trails[system_id].append(audit_event)
        
        # Keep only last 5000 events to prevent memory issues
        if len(self.audit_trails[system_id]) > 5000:
            self.audit_trails[system_id] = self.audit_trails[system_id][-5000:]
    
    def _check_monitoring_compliance(self, system_id: str) -> float:
        """Check monitoring compliance for a system."""
        # Mock implementation - would integrate with actual monitoring systems
        system_record = self.registered_systems[system_id]
        oversight_level = system_record["oversight_level"]
        
        # Base score based on oversight level implementation
        base_scores = {
            OversightLevel.BASIC.value: 80,
            OversightLevel.ENHANCED.value: 70,
            OversightLevel.COMPREHENSIVE.value: 60
        }
        
        return base_scores.get(oversight_level, 50)
    
    def _check_audit_compliance(self, system_id: str) -> float:
        """Check audit trail compliance for a system."""
        audit_events = self.audit_trails.get(system_id, [])
        
        if not audit_events:
            return 0
        
        # Check if recent audit events exist
        recent_events = [
            e for e in audit_events
            if (datetime.utcnow() - datetime.fromisoformat(e["timestamp"])).days <= 7
        ]
        
        if not recent_events:
            return 40  # Outdated audit trail
        
        return 90  # Good audit trail maintenance
    
    def _check_transparency_compliance(self, system_id: str) -> float:
        """Check transparency compliance for a system."""
        decisions = self.decision_logs.get(system_id, [])
        
        if not decisions:
            return 0
        
        # Check explanation coverage
        decisions_with_explanations = [d for d in decisions if d.get("explanation")]
        explanation_rate = len(decisions_with_explanations) / len(decisions)
        
        return explanation_rate * 100
    
    def _check_escalation_compliance(self, system_id: str) -> float:
        """Check escalation compliance for a system."""
        # Mock implementation - would check actual escalation handling
        return 85  # Assume good escalation compliance
    
    def _generate_oversight_recommendations(self, system_id: str, score: float) -> List[str]:
        """Generate oversight recommendations based on compliance score."""
        recommendations = []
        
        if score < 70:
            recommendations.append("Improve oversight compliance - score below threshold")
        
        if score < 50:
            recommendations.append("Immediate oversight review required")
        
        # Add specific recommendations based on compliance areas
        system_record = self.registered_systems[system_id]
        
        if not self.decision_logs.get(system_id):
            recommendations.append("Implement decision logging")
        
        if not self.audit_trails.get(system_id):
            recommendations.append("Establish audit trail procedures")
        
        return recommendations
    
    def _filter_decisions_by_date(self, system_id: str, start_date: str = None, end_date: str = None) -> List:
        """Filter decisions by date range."""
        decisions = self.decision_logs.get(system_id, [])
        
        if start_date:
            start_dt = datetime.fromisoformat(start_date)
            decisions = [d for d in decisions if datetime.fromisoformat(d["timestamp"]) >= start_dt]
        
        if end_date:
            end_dt = datetime.fromisoformat(end_date)
            decisions = [d for d in decisions if datetime.fromisoformat(d["timestamp"]) <= end_dt]
        
        return decisions
    
    def _analyze_decisions(self, decisions: List) -> Dict:
        """Analyze decisions for transparency reporting."""
        if not decisions:
            return {}
        
        # Decision type analysis
        decision_types = {}
        for decision in decisions:
            dtype = decision.get("decision_type", "unknown")
            decision_types[dtype] = decision_types.get(dtype, 0) + 1
        
        # Risk level distribution
        risk_distribution = {}
        for decision in decisions:
            risk = decision.get("risk_level", "unknown")
            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1
        
        # Confidence statistics
        confidences = [d.get("confidence") for d in decisions if d.get("confidence") is not None]
        confidence_stats = {}
        if confidences:
            confidence_stats = {
                "average": sum(confidences) / len(confidences),
                "min": min(confidences),
                "max": max(confidences)
            }
        
        # Human oversight rate
        human_decisions = [d for d in decisions if d.get("human_reviewer")]
        human_oversight_rate = len(human_decisions) / len(decisions) * 100
        
        # Explanation coverage
        explained_decisions = [d for d in decisions if d.get("explanation")]
        explanation_coverage = len(explained_decisions) / len(decisions) * 100
        
        # Mock escalation rate
        escalation_rate = 5.0  # 5% escalation rate
        
        return {
            "decision_types": decision_types,
            "risk_distribution": risk_distribution,
            "confidence_stats": confidence_stats,
            "human_oversight_rate": human_oversight_rate,
            "explanation_coverage": explanation_coverage,
            "escalation_rate": escalation_rate
        }
    
    def _generate_transparency_recommendations(self, analytics: Dict) -> List[str]:
        """Generate transparency recommendations based on decision analytics."""
        recommendations = []
        
        explanation_coverage = analytics.get("explanation_coverage", 0)
        if explanation_coverage < 80:
            recommendations.append(f"Improve explanation coverage (currently {explanation_coverage:.1f}%)")
        
        human_oversight_rate = analytics.get("human_oversight_rate", 0)
        if human_oversight_rate < 10:
            recommendations.append(f"Consider increasing human oversight (currently {human_oversight_rate:.1f}%)")
        
        escalation_rate = analytics.get("escalation_rate", 0)
        if escalation_rate > 15:
            recommendations.append("High escalation rate - review decision thresholds")
        elif escalation_rate < 2:
            recommendations.append("Low escalation rate - ensure escalation rules are working")
        
        return recommendations
    
    def _check_decision_escalation(self, system_id: str, decision_log: Dict):
        """Check if a decision should be escalated based on rules."""
        system_record = self.registered_systems[system_id]
        escalation_rules = system_record.get("escalation_rules", [])
        
        for rule in escalation_rules:
            condition = rule.get("condition", "")
            
            # Simple condition checking (would be more sophisticated in practice)
            confidence = decision_log.get("confidence", 1.0)
            if "confidence < 0.7" in condition and confidence < 0.7:
                self.escalate_decision(
                    system_id,
                    decision_log["decision_id"],
                    f"Low confidence: {confidence}",
                    "automated_system"
                )
                break