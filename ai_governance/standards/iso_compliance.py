"""
ISO Standards Compliance module for AI governance.

Implements compliance checks and assessments for ISO standards relevant
to AI governance, including ISO/IEC 23053, ISO/IEC 23901, ISO/IEC 23094,
and other relevant standards.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import json


class ISOStandard(Enum):
    """ISO standards relevant to AI governance."""
    ISO_IEC_23053 = "ISO/IEC 23053"  # Framework for AI risk management
    ISO_IEC_23901 = "ISO/IEC 23901"  # AI management system
    ISO_IEC_23094 = "ISO/IEC 23094"  # AI risk management
    ISO_IEC_27001 = "ISO/IEC 27001"  # Information security management
    ISO_9001 = "ISO 9001"            # Quality management systems


class ComplianceMaturity(Enum):
    """ISO compliance maturity levels."""
    INITIAL = "initial"
    DEVELOPING = "developing"
    DEFINED = "defined"
    MANAGED = "managed"
    OPTIMIZED = "optimized"


class ISOComplianceManager:
    """
    Manages ISO standards compliance for AI systems.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize the ISO compliance manager."""
        self.config = config or {}
        self.registered_systems: Dict[str, Dict] = {}
        self.compliance_assessments: Dict[str, List] = {}
        self.standard_requirements: Dict[str, Dict] = {}
        self.maturity_assessments: Dict[str, Dict] = {}
        
        # Initialize standard requirements
        self._initialize_standard_requirements()
        
    def register_system(self, system_id: str, system_info: Dict):
        """Register a system for ISO compliance management."""
        compliance_record = {
            "system_id": system_id,
            "system_name": system_info.get("name", system_id),
            "applicable_standards": self._determine_applicable_standards(system_info),
            "risk_level": system_info.get("risk_level", "medium"),
            "industry_sector": system_info.get("industry_sector", "general"),
            "registered_at": datetime.utcnow().isoformat(),
            "compliance_scope": self._define_compliance_scope(system_info),
            "target_maturity_level": self._determine_target_maturity(system_info)
        }
        
        self.registered_systems[system_id] = compliance_record
        self.compliance_assessments[system_id] = []
        self.maturity_assessments[system_id] = {}
    
    def assess_iso_compliance(self, system_id: str) -> Dict:
        """
        Assess ISO compliance for a registered system.
        
        Args:
            system_id: System identifier
            
        Returns:
            ISO compliance assessment results
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered", "score": 0}
        
        system_record = self.registered_systems[system_id]
        applicable_standards = system_record["applicable_standards"]
        
        # Assess compliance for each applicable standard
        standard_assessments = {}
        overall_scores = []
        
        for standard in applicable_standards:
            assessment = self._assess_standard_compliance(system_id, standard)
            standard_assessments[standard] = assessment
            overall_scores.append(assessment["score"])
        
        # Calculate overall compliance score
        overall_score = sum(overall_scores) / len(overall_scores) if overall_scores else 0
        
        # Assess maturity level
        maturity_assessment = self._assess_maturity_level(system_id)
        
        assessment = {
            "system_id": system_id,
            "assessed_at": datetime.utcnow().isoformat(),
            "applicable_standards": applicable_standards,
            "score": overall_score,
            "maturity_level": maturity_assessment["current_level"],
            "target_maturity_level": system_record["target_maturity_level"],
            "standard_assessments": standard_assessments,
            "maturity_assessment": maturity_assessment,
            "gaps_identified": self._identify_compliance_gaps(system_id, standard_assessments),
            "recommendations": self._generate_iso_recommendations(system_id, overall_score),
            "next_review_date": (datetime.utcnow() + timedelta(days=180)).isoformat()
        }
        
        # Store assessment
        self.compliance_assessments[system_id].append(assessment)
        
        return assessment
    
    def conduct_gap_analysis(self, system_id: str, standard: str) -> Dict:
        """
        Conduct detailed gap analysis for a specific ISO standard.
        
        Args:
            system_id: System identifier
            standard: ISO standard identifier
            
        Returns:
            Gap analysis results
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered"}
        
        if standard not in self.standard_requirements:
            return {"error": "Standard not supported"}
        
        requirements = self.standard_requirements[standard]
        system_record = self.registered_systems[system_id]
        
        gap_analysis = {
            "system_id": system_id,
            "standard": standard,
            "analyzed_at": datetime.utcnow().isoformat(),
            "requirements_analysis": {},
            "implementation_gaps": [],
            "priority_actions": [],
            "effort_estimation": {},
            "compliance_roadmap": []
        }
        
        # Analyze each requirement category
        for category, reqs in requirements.get("categories", {}).items():
            category_gaps = self._analyze_category_gaps(system_id, category, reqs)
            gap_analysis["requirements_analysis"][category] = category_gaps
            
            # Collect implementation gaps
            for gap in category_gaps.get("gaps", []):
                gap["category"] = category
                gap_analysis["implementation_gaps"].append(gap)
        
        # Prioritize actions
        gap_analysis["priority_actions"] = self._prioritize_gap_actions(gap_analysis["implementation_gaps"])
        
        # Estimate effort
        gap_analysis["effort_estimation"] = self._estimate_implementation_effort(gap_analysis["implementation_gaps"])
        
        # Create roadmap
        gap_analysis["compliance_roadmap"] = self._create_compliance_roadmap(gap_analysis["priority_actions"])
        
        return gap_analysis
    
    def track_compliance_progress(self, system_id: str, progress_data: Dict):
        """
        Track compliance implementation progress.
        
        Args:
            system_id: System identifier
            progress_data: Progress tracking data
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered"}
        
        progress_record = {
            "system_id": system_id,
            "updated_at": datetime.utcnow().isoformat(),
            "completed_actions": progress_data.get("completed_actions", []),
            "in_progress_actions": progress_data.get("in_progress_actions", []),
            "planned_actions": progress_data.get("planned_actions", []),
            "milestone_achievements": progress_data.get("milestones", []),
            "compliance_metrics": progress_data.get("metrics", {}),
            "challenges": progress_data.get("challenges", []),
            "next_steps": progress_data.get("next_steps", [])
        }
        
        # Update system record with progress
        system_record = self.registered_systems[system_id]
        if "compliance_progress" not in system_record:
            system_record["compliance_progress"] = []
        
        system_record["compliance_progress"].append(progress_record)
        
        # Update maturity level if significant progress made
        self._update_maturity_level(system_id, progress_data)
        
        return {"status": "tracked", "progress_id": f"progress_{int(datetime.utcnow().timestamp())}"}
    
    def generate_compliance_report(self, system_id: str = None, standard: str = None) -> Dict:
        """
        Generate comprehensive ISO compliance report.
        
        Args:
            system_id: Optional system identifier to filter by
            standard: Optional standard to filter by
            
        Returns:
            Compliance report
        """
        if system_id and system_id not in self.registered_systems:
            return {"error": "System not registered"}
        
        # Filter systems if specified
        if system_id:
            systems = {system_id: self.registered_systems[system_id]}
        else:
            systems = self.registered_systems
        
        # Aggregate compliance data
        compliance_summary = {
            "total_systems": len(systems),
            "standards_coverage": {},
            "maturity_distribution": {},
            "compliance_scores": []
        }
        
        system_details = []
        
        for sid, system_record in systems.items():
            # Get latest assessment
            assessments = self.compliance_assessments.get(sid, [])
            latest_assessment = assessments[-1] if assessments else None
            
            if latest_assessment:
                compliance_summary["compliance_scores"].append(latest_assessment["score"])
                
                # Aggregate standards coverage
                for std in latest_assessment["applicable_standards"]:
                    if standard and std != standard:
                        continue
                    compliance_summary["standards_coverage"][std] = \
                        compliance_summary["standards_coverage"].get(std, 0) + 1
                
                # Aggregate maturity levels
                maturity = latest_assessment["maturity_level"]
                compliance_summary["maturity_distribution"][maturity] = \
                    compliance_summary["maturity_distribution"].get(maturity, 0) + 1
            
            # Add system details
            system_details.append({
                "system_id": sid,
                "system_name": system_record["system_name"],
                "applicable_standards": system_record["applicable_standards"],
                "compliance_score": latest_assessment["score"] if latest_assessment else None,
                "maturity_level": latest_assessment["maturity_level"] if latest_assessment else "unknown",
                "last_assessed": latest_assessment["assessed_at"] if latest_assessment else None
            })
        
        # Calculate average compliance score
        if compliance_summary["compliance_scores"]:
            compliance_summary["average_compliance_score"] = \
                sum(compliance_summary["compliance_scores"]) / len(compliance_summary["compliance_scores"])
        
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "scope": {
                "system_filter": system_id,
                "standard_filter": standard
            },
            "compliance_summary": compliance_summary,
            "system_details": system_details,
            "recommendations": self._generate_organization_recommendations(compliance_summary)
        }
        
        return report
    
    def _initialize_standard_requirements(self):
        """Initialize requirements for supported ISO standards."""
        
        # ISO/IEC 23053 - Framework for AI risk management
        self.standard_requirements[ISOStandard.ISO_IEC_23053.value] = {
            "title": "Framework for AI risk management",
            "categories": {
                "risk_identification": {
                    "requirements": [
                        "Establish AI risk identification processes",
                        "Identify potential AI-related risks",
                        "Document risk scenarios",
                        "Maintain risk register"
                    ]
                },
                "risk_assessment": {
                    "requirements": [
                        "Assess probability and impact of AI risks",
                        "Classify risks by severity",
                        "Evaluate risk interdependencies",
                        "Document assessment methodology"
                    ]
                },
                "risk_treatment": {
                    "requirements": [
                        "Develop risk mitigation strategies",
                        "Implement risk controls",
                        "Monitor control effectiveness",
                        "Update treatment plans"
                    ]
                },
                "governance": {
                    "requirements": [
                        "Establish AI risk governance framework",
                        "Define roles and responsibilities",
                        "Implement oversight mechanisms",
                        "Regular governance reviews"
                    ]
                }
            }
        }
        
        # ISO/IEC 23901 - AI management system
        self.standard_requirements[ISOStandard.ISO_IEC_23901.value] = {
            "title": "AI management system",
            "categories": {
                "management_system": {
                    "requirements": [
                        "Establish AI management system",
                        "Define AI policy and objectives",
                        "Document management processes",
                        "Implement continuous improvement"
                    ]
                },
                "planning": {
                    "requirements": [
                        "AI system planning processes",
                        "Resource allocation planning",
                        "Risk and opportunity planning",
                        "Objective setting and monitoring"
                    ]
                },
                "operation": {
                    "requirements": [
                        "AI system development controls",
                        "Operational procedures",
                        "Change management",
                        "Incident management"
                    ]
                },
                "performance_evaluation": {
                    "requirements": [
                        "Monitor AI system performance",
                        "Conduct internal audits",
                        "Management reviews",
                        "Measure objective achievement"
                    ]
                }
            }
        }
        
        # Additional standards would be defined similarly...
    
    def _determine_applicable_standards(self, system_info: Dict) -> List[str]:
        """Determine which ISO standards apply to a system."""
        standards = []
        
        # All AI systems should consider risk management
        standards.append(ISOStandard.ISO_IEC_23053.value)
        
        # High-risk systems need management system
        risk_level = system_info.get("risk_level", "medium")
        if risk_level in ["high", "critical"]:
            standards.append(ISOStandard.ISO_IEC_23901.value)
        
        # Financial services need additional standards
        industry = system_info.get("industry_sector", "")
        if "financial" in industry.lower():
            standards.append(ISOStandard.ISO_IEC_27001.value)
        
        # Quality-critical systems
        if system_info.get("quality_critical", False):
            standards.append(ISOStandard.ISO_9001.value)
        
        return standards
    
    def _define_compliance_scope(self, system_info: Dict) -> Dict:
        """Define the scope of compliance for a system."""
        return {
            "ai_components": system_info.get("ai_components", []),
            "data_processing": system_info.get("data_processing", True),
            "model_lifecycle": system_info.get("model_lifecycle", True),
            "infrastructure": system_info.get("infrastructure_scope", False),
            "third_party_integrations": system_info.get("third_party", [])
        }
    
    def _determine_target_maturity(self, system_info: Dict) -> str:
        """Determine target maturity level for a system."""
        risk_level = system_info.get("risk_level", "medium")
        industry = system_info.get("industry_sector", "")
        
        if risk_level == "critical" or "financial" in industry.lower():
            return ComplianceMaturity.OPTIMIZED.value
        elif risk_level == "high":
            return ComplianceMaturity.MANAGED.value
        elif risk_level == "medium":
            return ComplianceMaturity.DEFINED.value
        else:
            return ComplianceMaturity.DEVELOPING.value
    
    def _assess_standard_compliance(self, system_id: str, standard: str) -> Dict:
        """Assess compliance for a specific standard."""
        if standard not in self.standard_requirements:
            return {"error": "Standard not supported", "score": 0}
        
        requirements = self.standard_requirements[standard]
        
        # Mock assessment - in practice, this would involve detailed evaluation
        assessment = {
            "standard": standard,
            "assessed_at": datetime.utcnow().isoformat(),
            "score": 0,
            "category_scores": {},
            "compliant_requirements": [],
            "non_compliant_requirements": [],
            "partially_compliant_requirements": []
        }
        
        category_scores = []
        
        for category, category_data in requirements.get("categories", {}).items():
            # Mock category assessment
            category_score = self._assess_category_compliance(system_id, category, category_data)
            category_scores.append(category_score)
            assessment["category_scores"][category] = category_score
        
        # Calculate overall score
        assessment["score"] = sum(category_scores) / len(category_scores) if category_scores else 0
        
        return assessment
    
    def _assess_category_compliance(self, system_id: str, category: str, category_data: Dict) -> float:
        """Assess compliance for a specific category."""
        # Mock implementation - would involve actual assessment logic
        system_record = self.registered_systems[system_id]
        risk_level = system_record.get("risk_level", "medium")
        
        # Base score varies by risk level and category
        base_scores = {
            "low": {"risk_identification": 80, "risk_assessment": 75, "risk_treatment": 70, "governance": 65},
            "medium": {"risk_identification": 70, "risk_assessment": 65, "risk_treatment": 60, "governance": 55},
            "high": {"risk_identification": 60, "risk_assessment": 55, "risk_treatment": 50, "governance": 45},
            "critical": {"risk_identification": 50, "risk_assessment": 45, "risk_treatment": 40, "governance": 35}
        }
        
        return base_scores.get(risk_level, {}).get(category, 50)
    
    def _assess_maturity_level(self, system_id: str) -> Dict:
        """Assess the current maturity level of a system."""
        assessments = self.compliance_assessments.get(system_id, [])
        
        if not assessments:
            current_level = ComplianceMaturity.INITIAL.value
            maturity_score = 0
        else:
            latest_assessment = assessments[-1]
            score = latest_assessment["score"]
            
            if score >= 90:
                current_level = ComplianceMaturity.OPTIMIZED.value
                maturity_score = score
            elif score >= 75:
                current_level = ComplianceMaturity.MANAGED.value
                maturity_score = score
            elif score >= 60:
                current_level = ComplianceMaturity.DEFINED.value
                maturity_score = score
            elif score >= 40:
                current_level = ComplianceMaturity.DEVELOPING.value
                maturity_score = score
            else:
                current_level = ComplianceMaturity.INITIAL.value
                maturity_score = score
        
        return {
            "current_level": current_level,
            "maturity_score": maturity_score,
            "assessed_at": datetime.utcnow().isoformat()
        }
    
    def _identify_compliance_gaps(self, system_id: str, standard_assessments: Dict) -> List[Dict]:
        """Identify compliance gaps across all standards."""
        gaps = []
        
        for standard, assessment in standard_assessments.items():
            if assessment["score"] < 80:  # Compliance threshold
                gaps.append({
                    "standard": standard,
                    "gap_type": "overall_compliance",
                    "current_score": assessment["score"],
                    "target_score": 80,
                    "priority": "high" if assessment["score"] < 60 else "medium"
                })
            
            # Check category-specific gaps
            for category, score in assessment.get("category_scores", {}).items():
                if score < 70:  # Category threshold
                    gaps.append({
                        "standard": standard,
                        "category": category,
                        "gap_type": "category_compliance",
                        "current_score": score,
                        "target_score": 70,
                        "priority": "high" if score < 50 else "medium"
                    })
        
        return gaps
    
    def _generate_iso_recommendations(self, system_id: str, score: float) -> List[str]:
        """Generate ISO compliance recommendations."""
        recommendations = []
        
        if score < 70:
            recommendations.append("Implement comprehensive compliance improvement program")
        
        if score < 50:
            recommendations.append("Conduct urgent compliance remediation")
        
        # Add specific recommendations based on system characteristics
        system_record = self.registered_systems[system_id]
        
        if system_record.get("risk_level") in ["high", "critical"]:
            recommendations.append("Implement enhanced governance and oversight mechanisms")
        
        # Check for missing standards
        applicable_standards = system_record["applicable_standards"]
        if len(applicable_standards) < 2:
            recommendations.append("Evaluate additional applicable ISO standards")
        
        return recommendations
    
    def _analyze_category_gaps(self, system_id: str, category: str, requirements: Dict) -> Dict:
        """Analyze gaps for a specific requirement category."""
        # Mock implementation
        gaps = []
        implemented = []
        
        for req in requirements.get("requirements", []):
            # Mock assessment of each requirement
            implementation_status = self._assess_requirement_implementation(system_id, req)
            
            if implementation_status["status"] == "not_implemented":
                gaps.append({
                    "requirement": req,
                    "status": "not_implemented",
                    "priority": implementation_status["priority"],
                    "effort": implementation_status["effort"]
                })
            else:
                implemented.append({
                    "requirement": req,
                    "status": implementation_status["status"]
                })
        
        return {
            "category": category,
            "total_requirements": len(requirements.get("requirements", [])),
            "implemented": len(implemented),
            "gaps": gaps,
            "implementation_rate": len(implemented) / len(requirements.get("requirements", [])) * 100 if requirements.get("requirements") else 0
        }
    
    def _assess_requirement_implementation(self, system_id: str, requirement: str) -> Dict:
        """Assess implementation status of a specific requirement."""
        # Mock implementation - would involve actual system assessment
        return {
            "requirement": requirement,
            "status": "partially_implemented",  # Mock status
            "priority": "medium",
            "effort": "moderate"
        }
    
    def _prioritize_gap_actions(self, gaps: List[Dict]) -> List[Dict]:
        """Prioritize gap remediation actions."""
        # Sort by priority and effort
        priority_order = {"high": 3, "medium": 2, "low": 1}
        effort_order = {"low": 1, "moderate": 2, "high": 3}
        
        return sorted(gaps, key=lambda x: (
            -priority_order.get(x.get("priority", "medium"), 2),
            effort_order.get(x.get("effort", "moderate"), 2)
        ))
    
    def _estimate_implementation_effort(self, gaps: List[Dict]) -> Dict:
        """Estimate effort required to address gaps."""
        effort_mapping = {"low": 1, "moderate": 3, "high": 5}
        
        total_effort = sum(effort_mapping.get(gap.get("effort", "moderate"), 3) for gap in gaps)
        
        return {
            "total_effort_points": total_effort,
            "estimated_weeks": total_effort * 2,  # Assume 2 weeks per effort point
            "effort_breakdown": {
                "high_effort": len([g for g in gaps if g.get("effort") == "high"]),
                "moderate_effort": len([g for g in gaps if g.get("effort") == "moderate"]),
                "low_effort": len([g for g in gaps if g.get("effort") == "low"])
            }
        }
    
    def _create_compliance_roadmap(self, priority_actions: List[Dict]) -> List[Dict]:
        """Create implementation roadmap for compliance."""
        roadmap = []
        current_week = 0
        
        for i, action in enumerate(priority_actions[:10]):  # Top 10 actions
            effort_weeks = {"low": 2, "moderate": 4, "high": 8}.get(action.get("effort", "moderate"), 4)
            
            roadmap.append({
                "phase": f"Phase {i // 3 + 1}",
                "action": action.get("requirement", "Unknown action"),
                "start_week": current_week,
                "duration_weeks": effort_weeks,
                "priority": action.get("priority", "medium"),
                "dependencies": []
            })
            
            current_week += effort_weeks
        
        return roadmap
    
    def _update_maturity_level(self, system_id: str, progress_data: Dict):
        """Update maturity level based on progress."""
        completed_actions = len(progress_data.get("completed_actions", []))
        
        # Simple maturity progression based on completed actions
        if completed_actions >= 20:
            new_level = ComplianceMaturity.OPTIMIZED.value
        elif completed_actions >= 15:
            new_level = ComplianceMaturity.MANAGED.value
        elif completed_actions >= 10:
            new_level = ComplianceMaturity.DEFINED.value
        elif completed_actions >= 5:
            new_level = ComplianceMaturity.DEVELOPING.value
        else:
            new_level = ComplianceMaturity.INITIAL.value
        
        self.maturity_assessments[system_id] = {
            "level": new_level,
            "updated_at": datetime.utcnow().isoformat(),
            "completed_actions": completed_actions
        }
    
    def _generate_organization_recommendations(self, compliance_summary: Dict) -> List[str]:
        """Generate organization-level recommendations."""
        recommendations = []
        
        avg_score = compliance_summary.get("average_compliance_score", 0)
        if avg_score < 70:
            recommendations.append("Implement organization-wide ISO compliance improvement program")
        
        standards_coverage = compliance_summary.get("standards_coverage", {})
        if len(standards_coverage) < 3:
            recommendations.append("Expand ISO standards coverage across organization")
        
        maturity_dist = compliance_summary.get("maturity_distribution", {})
        initial_systems = maturity_dist.get(ComplianceMaturity.INITIAL.value, 0)
        total_systems = compliance_summary.get("total_systems", 1)
        
        if initial_systems / total_systems > 0.3:
            recommendations.append("Focus on advancing systems from initial maturity level")
        
        return recommendations