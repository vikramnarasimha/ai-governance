"""
Core governance framework that integrates all governance modules.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json

from .model_risk_management import ModelRiskManager
from .ai_oversight import AIOversightManager
from .data_governance import DataGovernanceManager
from .data_residency import DataResidencyManager
from ..standards.iso_compliance import ISOComplianceManager


class GovernanceLevel(Enum):
    """Governance levels for different types of AI systems."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class GovernanceFramework:
    """
    Main governance framework that orchestrates all governance modules
    for AI systems in financial services institutions.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the governance framework with configuration."""
        self.config = config or {}
        self.created_at = datetime.utcnow()
        
        # Initialize governance modules
        self.model_risk_manager = ModelRiskManager(self.config.get("model_risk", {}))
        self.ai_oversight_manager = AIOversightManager(self.config.get("ai_oversight", {}))
        self.data_governance_manager = DataGovernanceManager(self.config.get("data_governance", {}))
        self.data_residency_manager = DataResidencyManager(self.config.get("data_residency", {}))
        self.iso_compliance_manager = ISOComplianceManager(self.config.get("iso_compliance", {}))
        
        # Track registered AI systems
        self.registered_systems: Dict[str, Dict] = {}
        
    def register_ai_system(self, system_id: str, system_info: Dict) -> Dict:
        """
        Register a new AI system for governance.
        
        Args:
            system_id: Unique identifier for the AI system
            system_info: Dictionary containing system metadata
            
        Returns:
            Registration response with governance requirements
        """
        # Determine governance level based on system criticality
        governance_level = self._assess_governance_level(system_info)
        
        # Create governance record
        governance_record = {
            "system_id": system_id,
            "system_info": system_info,
            "governance_level": governance_level.value,
            "registered_at": datetime.utcnow().isoformat(),
            "status": "registered",
            "compliance_status": {},
            "governance_requirements": self._generate_governance_requirements(governance_level)
        }
        
        # Store registration
        self.registered_systems[system_id] = governance_record
        
        # Initialize governance assessments
        self._initialize_assessments(system_id, system_info)
        
        return {
            "status": "success",
            "system_id": system_id,
            "governance_level": governance_level.value,
            "requirements": governance_record["governance_requirements"]
        }
    
    def assess_system_compliance(self, system_id: str) -> Dict:
        """
        Comprehensive compliance assessment for a registered AI system.
        
        Args:
            system_id: Unique identifier for the AI system
            
        Returns:
            Compliance assessment results
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered"}
        
        system_record = self.registered_systems[system_id]
        
        # Run assessments across all governance modules
        assessments = {
            "model_risk": self.model_risk_manager.assess_model_risk(system_id),
            "ai_oversight": self.ai_oversight_manager.assess_oversight_compliance(system_id),
            "data_governance": self.data_governance_manager.assess_data_compliance(system_id),
            "data_residency": self.data_residency_manager.assess_residency_compliance(system_id),
            "iso_compliance": self.iso_compliance_manager.assess_iso_compliance(system_id)
        }
        
        # Calculate overall compliance score
        overall_score = self._calculate_overall_compliance(assessments)
        
        # Update system record
        system_record["compliance_status"] = {
            "last_assessed": datetime.utcnow().isoformat(),
            "overall_score": overall_score,
            "module_assessments": assessments,
            "status": "compliant" if overall_score >= 80 else "non_compliant"
        }
        
        return system_record["compliance_status"]
    
    def get_governance_dashboard(self) -> Dict:
        """
        Generate governance dashboard data.
        
        Returns:
            Dashboard data with key metrics and status
        """
        total_systems = len(self.registered_systems)
        compliant_systems = sum(1 for system in self.registered_systems.values() 
                              if system.get("compliance_status", {}).get("status") == "compliant")
        
        # Governance level distribution
        level_distribution = {}
        for system in self.registered_systems.values():
            level = system["governance_level"]
            level_distribution[level] = level_distribution.get(level, 0) + 1
        
        # Recent assessments
        recent_assessments = []
        for system_id, system in self.registered_systems.items():
            if "compliance_status" in system:
                recent_assessments.append({
                    "system_id": system_id,
                    "score": system["compliance_status"]["overall_score"],
                    "status": system["compliance_status"]["status"],
                    "assessed_at": system["compliance_status"]["last_assessed"]
                })
        
        return {
            "summary": {
                "total_systems": total_systems,
                "compliant_systems": compliant_systems,
                "compliance_rate": (compliant_systems / total_systems * 100) if total_systems > 0 else 0
            },
            "governance_levels": level_distribution,
            "recent_assessments": sorted(recent_assessments, 
                                       key=lambda x: x["assessed_at"], 
                                       reverse=True)[:10]
        }
    
    def _assess_governance_level(self, system_info: Dict) -> GovernanceLevel:
        """Assess the governance level required for a system."""
        # Simple rule-based assessment (could be enhanced with ML)
        risk_factors = system_info.get("risk_factors", [])
        use_case = system_info.get("use_case", "").lower()
        data_sensitivity = system_info.get("data_sensitivity", "medium").lower()
        
        score = 0
        
        # High-risk use cases
        high_risk_use_cases = ["credit_scoring", "fraud_detection", "compliance", "regulatory"]
        if any(case in use_case for case in high_risk_use_cases):
            score += 3
        
        # Data sensitivity
        if data_sensitivity == "high":
            score += 2
        elif data_sensitivity == "medium":
            score += 1
        
        # Risk factors
        score += len(risk_factors)
        
        if score >= 5:
            return GovernanceLevel.CRITICAL
        elif score >= 3:
            return GovernanceLevel.HIGH
        elif score >= 1:
            return GovernanceLevel.MEDIUM
        else:
            return GovernanceLevel.LOW
    
    def _generate_governance_requirements(self, level: GovernanceLevel) -> List[str]:
        """Generate governance requirements based on level."""
        base_requirements = [
            "Model documentation",
            "Data lineage tracking",
            "Basic monitoring"
        ]
        
        if level in [GovernanceLevel.MEDIUM, GovernanceLevel.HIGH, GovernanceLevel.CRITICAL]:
            base_requirements.extend([
                "Model validation",
                "Bias testing",
                "Performance monitoring"
            ])
        
        if level in [GovernanceLevel.HIGH, GovernanceLevel.CRITICAL]:
            base_requirements.extend([
                "Third-party model validation",
                "Explainability analysis",
                "Regulatory compliance review"
            ])
        
        if level == GovernanceLevel.CRITICAL:
            base_requirements.extend([
                "Board-level oversight",
                "Continuous monitoring",
                "Incident response plan"
            ])
        
        return base_requirements
    
    def _initialize_assessments(self, system_id: str, system_info: Dict):
        """Initialize assessments for all governance modules."""
        # Initialize each module with system information
        self.model_risk_manager.register_system(system_id, system_info)
        self.ai_oversight_manager.register_system(system_id, system_info)
        self.data_governance_manager.register_system(system_id, system_info)
        self.data_residency_manager.register_system(system_id, system_info)
        self.iso_compliance_manager.register_system(system_id, system_info)
    
    def _calculate_overall_compliance(self, assessments: Dict) -> float:
        """Calculate overall compliance score from module assessments."""
        scores = []
        weights = {
            "model_risk": 0.25,
            "ai_oversight": 0.2,
            "data_governance": 0.2,
            "data_residency": 0.15,
            "iso_compliance": 0.2
        }
        
        weighted_score = 0
        total_weight = 0
        
        for module, assessment in assessments.items():
            if "score" in assessment and module in weights:
                weighted_score += assessment["score"] * weights[module]
                total_weight += weights[module]
        
        return weighted_score / total_weight if total_weight > 0 else 0