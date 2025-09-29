"""
Data Governance module for managing data quality, lineage, and compliance.

Implements comprehensive data governance practices including data quality
monitoring, lineage tracking, privacy compliance, and data lifecycle management.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import json


class DataClassification(Enum):
    """Data classification levels."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class DataQualityStatus(Enum):
    """Data quality status levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class DataGovernanceManager:
    """
    Manages data governance including quality, lineage, and compliance.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize the data governance manager."""
        self.config = config or {}
        self.registered_systems: Dict[str, Dict] = {}
        self.data_assets: Dict[str, Dict] = {}
        self.quality_reports: Dict[str, List] = {}
        self.lineage_records: Dict[str, Dict] = {}
        self.compliance_records: Dict[str, List] = {}
        
    def register_system(self, system_id: str, system_info: Dict):
        """Register a system for data governance."""
        governance_record = {
            "system_id": system_id,
            "system_name": system_info.get("name", system_id),
            "data_sources": system_info.get("data_sources", []),
            "data_types": system_info.get("data_types", []),
            "data_classification": self._classify_data(system_info),
            "registered_at": datetime.utcnow().isoformat(),
            "governance_requirements": self._get_data_governance_requirements(system_info),
            "privacy_requirements": self._get_privacy_requirements(system_info),
            "retention_policy": self._get_retention_policy(system_info)
        }
        
        self.registered_systems[system_id] = governance_record
        self.quality_reports[system_id] = []
        self.compliance_records[system_id] = []
        
        # Initialize data assets for each data source
        for source in governance_record["data_sources"]:
            asset_id = f"{system_id}_{source}"
            self.data_assets[asset_id] = {
                "asset_id": asset_id,
                "system_id": system_id,
                "source_name": source,
                "classification": governance_record["data_classification"],
                "created_at": datetime.utcnow().isoformat(),
                "last_updated": datetime.utcnow().isoformat()
            }
    
    def assess_data_compliance(self, system_id: str) -> Dict:
        """
        Assess data governance compliance for a registered system.
        
        Args:
            system_id: System identifier
            
        Returns:
            Data governance compliance assessment
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered", "score": 0}
        
        system_record = self.registered_systems[system_id]
        
        # Check various compliance aspects
        quality_compliance = self._check_data_quality_compliance(system_id)
        lineage_compliance = self._check_lineage_compliance(system_id)
        privacy_compliance = self._check_privacy_compliance(system_id)
        retention_compliance = self._check_retention_compliance(system_id)
        
        # Calculate overall compliance score
        overall_score = (
            quality_compliance * 0.3 +
            lineage_compliance * 0.25 +
            privacy_compliance * 0.25 +
            retention_compliance * 0.2
        )
        
        assessment = {
            "system_id": system_id,
            "assessed_at": datetime.utcnow().isoformat(),
            "data_classification": system_record["data_classification"],
            "score": overall_score,
            "compliance_areas": {
                "data_quality": quality_compliance,
                "data_lineage": lineage_compliance,
                "privacy_compliance": privacy_compliance,
                "retention_compliance": retention_compliance
            },
            "data_assets_count": len([a for a in self.data_assets.values() if a["system_id"] == system_id]),
            "recommendations": self._generate_data_recommendations(system_id, overall_score),
            "next_review_date": (datetime.utcnow() + timedelta(days=60)).isoformat()
        }
        
        return assessment
    
    def assess_data_quality(self, system_id: str, data_source: str, quality_metrics: Dict) -> Dict:
        """
        Assess data quality for a specific data source.
        
        Args:
            system_id: System identifier
            data_source: Data source name
            quality_metrics: Quality metrics data
            
        Returns:
            Data quality assessment results
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered"}
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(quality_metrics)
        quality_status = self._determine_quality_status(quality_score)
        
        quality_report = {
            "report_id": f"dq_{system_id}_{data_source}_{int(datetime.utcnow().timestamp())}",
            "system_id": system_id,
            "data_source": data_source,
            "assessed_at": datetime.utcnow().isoformat(),
            "quality_score": quality_score,
            "quality_status": quality_status.value,
            "metrics": quality_metrics,
            "dimensions": {
                "completeness": quality_metrics.get("completeness", 0),
                "accuracy": quality_metrics.get("accuracy", 0),
                "consistency": quality_metrics.get("consistency", 0),
                "timeliness": quality_metrics.get("timeliness", 0),
                "validity": quality_metrics.get("validity", 0),
                "uniqueness": quality_metrics.get("uniqueness", 0)
            },
            "issues": self._identify_quality_issues(quality_metrics),
            "recommendations": self._generate_quality_recommendations(quality_metrics)
        }
        
        # Store quality report
        self.quality_reports[system_id].append(quality_report)
        
        # Update data asset
        asset_id = f"{system_id}_{data_source}"
        if asset_id in self.data_assets:
            self.data_assets[asset_id].update({
                "last_quality_check": datetime.utcnow().isoformat(),
                "quality_score": quality_score,
                "quality_status": quality_status.value
            })
        
        return quality_report
    
    def track_data_lineage(self, system_id: str, lineage_data: Dict):
        """
        Track data lineage for a system.
        
        Args:
            system_id: System identifier
            lineage_data: Data lineage information
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered"}
        
        lineage_record = {
            "system_id": system_id,
            "tracked_at": datetime.utcnow().isoformat(),
            "data_flow": lineage_data.get("data_flow", []),
            "transformations": lineage_data.get("transformations", []),
            "dependencies": lineage_data.get("dependencies", []),
            "impact_analysis": self._analyze_lineage_impact(lineage_data)
        }
        
        self.lineage_records[system_id] = lineage_record
        return {"status": "tracked", "lineage_id": f"lineage_{system_id}"}
    
    def check_privacy_compliance(self, system_id: str, privacy_data: Dict) -> Dict:
        """
        Check privacy compliance for a system.
        
        Args:
            system_id: System identifier
            privacy_data: Privacy compliance data
            
        Returns:
            Privacy compliance assessment
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered"}
        
        system_record = self.registered_systems[system_id]
        
        compliance_check = {
            "system_id": system_id,
            "checked_at": datetime.utcnow().isoformat(),
            "data_classification": system_record["data_classification"],
            "privacy_requirements": system_record["privacy_requirements"],
            "compliance_status": {},
            "violations": [],
            "recommendations": []
        }
        
        # Check GDPR compliance
        gdpr_compliance = self._check_gdpr_compliance(privacy_data)
        compliance_check["compliance_status"]["gdpr"] = gdpr_compliance
        
        # Check CCPA compliance
        ccpa_compliance = self._check_ccpa_compliance(privacy_data)
        compliance_check["compliance_status"]["ccpa"] = ccpa_compliance
        
        # Check data minimization
        minimization_compliance = self._check_data_minimization(privacy_data)
        compliance_check["compliance_status"]["data_minimization"] = minimization_compliance
        
        # Check consent management
        consent_compliance = self._check_consent_management(privacy_data)
        compliance_check["compliance_status"]["consent_management"] = consent_compliance
        
        # Generate overall compliance score
        compliance_scores = [
            gdpr_compliance.get("score", 0),
            ccpa_compliance.get("score", 0),
            minimization_compliance.get("score", 0),
            consent_compliance.get("score", 0)
        ]
        compliance_check["overall_score"] = sum(compliance_scores) / len(compliance_scores)
        
        # Store compliance record
        self.compliance_records[system_id].append(compliance_check)
        
        return compliance_check
    
    def generate_data_inventory(self, system_id: str = None) -> Dict:
        """
        Generate data inventory report.
        
        Args:
            system_id: Optional system identifier to filter by
            
        Returns:
            Data inventory report
        """
        if system_id and system_id not in self.registered_systems:
            return {"error": "System not registered"}
        
        # Filter assets by system if specified
        if system_id:
            assets = {k: v for k, v in self.data_assets.items() if v["system_id"] == system_id}
        else:
            assets = self.data_assets
        
        # Categorize assets by classification
        classification_summary = {}
        for asset in assets.values():
            classification = asset["classification"]
            if classification not in classification_summary:
                classification_summary[classification] = {
                    "count": 0,
                    "assets": []
                }
            classification_summary[classification]["count"] += 1
            classification_summary[classification]["assets"].append(asset["asset_id"])
        
        # Quality summary
        quality_summary = {}
        for asset in assets.values():
            status = asset.get("quality_status", "unknown")
            quality_summary[status] = quality_summary.get(status, 0) + 1
        
        inventory = {
            "generated_at": datetime.utcnow().isoformat(),
            "scope": f"system_{system_id}" if system_id else "all_systems",
            "summary": {
                "total_assets": len(assets),
                "classification_breakdown": classification_summary,
                "quality_breakdown": quality_summary
            },
            "assets": list(assets.values())
        }
        
        return inventory
    
    def _classify_data(self, system_info: Dict) -> str:
        """Classify data based on system information."""
        data_types = system_info.get("data_types", [])
        use_case = system_info.get("use_case", "").lower()
        
        # Check for sensitive data types
        sensitive_types = ["pii", "financial", "health", "biometric"]
        if any(dtype.lower() in sensitive_types for dtype in data_types):
            return DataClassification.RESTRICTED.value
        
        # Check use case sensitivity
        if any(case in use_case for case in ["compliance", "regulatory", "credit"]):
            return DataClassification.CONFIDENTIAL.value
        
        # Default classification
        return DataClassification.INTERNAL.value
    
    def _get_data_governance_requirements(self, system_info: Dict) -> List[str]:
        """Get data governance requirements based on system information."""
        classification = self._classify_data(system_info)
        
        base_requirements = [
            "data_catalog",
            "quality_monitoring",
            "basic_lineage"
        ]
        
        if classification in [DataClassification.CONFIDENTIAL.value, DataClassification.RESTRICTED.value]:
            base_requirements.extend([
                "comprehensive_lineage",
                "access_controls",
                "audit_logging"
            ])
        
        if classification == DataClassification.RESTRICTED.value:
            base_requirements.extend([
                "encryption_at_rest",
                "encryption_in_transit",
                "privacy_compliance",
                "data_masking"
            ])
        
        return base_requirements
    
    def _get_privacy_requirements(self, system_info: Dict) -> List[str]:
        """Get privacy requirements based on system information."""
        data_types = system_info.get("data_types", [])
        jurisdiction = system_info.get("jurisdiction", [])
        
        requirements = []
        
        # Check for PII
        if "pii" in [dtype.lower() for dtype in data_types]:
            requirements.extend([
                "consent_management",
                "data_subject_rights",
                "purpose_limitation"
            ])
        
        # Jurisdiction-specific requirements
        if "eu" in [j.lower() for j in jurisdiction]:
            requirements.extend(["gdpr_compliance", "right_to_be_forgotten"])
        
        if "california" in [j.lower() for j in jurisdiction]:
            requirements.append("ccpa_compliance")
        
        return requirements
    
    def _get_retention_policy(self, system_info: Dict) -> Dict:
        """Get data retention policy based on system information."""
        use_case = system_info.get("use_case", "").lower()
        data_types = system_info.get("data_types", [])
        
        # Default retention policy
        policy = {
            "retention_period": "7_years",
            "deletion_method": "secure_deletion",
            "archive_requirements": True
        }
        
        # Adjust based on use case
        if "compliance" in use_case:
            policy["retention_period"] = "10_years"
        elif "analytics" in use_case:
            policy["retention_period"] = "3_years"
        
        # Adjust based on data types
        if "pii" in [dtype.lower() for dtype in data_types]:
            policy["special_handling"] = True
            policy["anonymization_required"] = True
        
        return policy
    
    def _calculate_quality_score(self, quality_metrics: Dict) -> float:
        """Calculate overall data quality score."""
        dimensions = [
            "completeness", "accuracy", "consistency", 
            "timeliness", "validity", "uniqueness"
        ]
        
        scores = []
        for dimension in dimensions:
            score = quality_metrics.get(dimension, 0)
            scores.append(score)
        
        return sum(scores) / len(scores) if scores else 0
    
    def _determine_quality_status(self, score: float) -> DataQualityStatus:
        """Determine quality status based on score."""
        if score >= 90:
            return DataQualityStatus.EXCELLENT
        elif score >= 75:
            return DataQualityStatus.GOOD
        elif score >= 50:
            return DataQualityStatus.FAIR
        else:
            return DataQualityStatus.POOR
    
    def _identify_quality_issues(self, quality_metrics: Dict) -> List[str]:
        """Identify data quality issues."""
        issues = []
        
        if quality_metrics.get("completeness", 100) < 95:
            issues.append("Data completeness below threshold")
        
        if quality_metrics.get("accuracy", 100) < 90:
            issues.append("Data accuracy concerns detected")
        
        if quality_metrics.get("consistency", 100) < 85:
            issues.append("Data consistency issues found")
        
        if quality_metrics.get("timeliness", 100) < 80:
            issues.append("Data timeliness issues detected")
        
        return issues
    
    def _generate_quality_recommendations(self, quality_metrics: Dict) -> List[str]:
        """Generate data quality recommendations."""
        recommendations = []
        
        if quality_metrics.get("completeness", 100) < 95:
            recommendations.append("Implement data validation rules to improve completeness")
        
        if quality_metrics.get("accuracy", 100) < 90:
            recommendations.append("Review data entry processes and validation controls")
        
        if quality_metrics.get("consistency", 100) < 85:
            recommendations.append("Standardize data formats and reference data")
        
        return recommendations
    
    def _check_data_quality_compliance(self, system_id: str) -> float:
        """Check data quality compliance for a system."""
        quality_reports = self.quality_reports.get(system_id, [])
        
        if not quality_reports:
            return 0  # No quality assessments
        
        # Get recent quality reports (last 30 days)
        recent_reports = [
            r for r in quality_reports
            if (datetime.utcnow() - datetime.fromisoformat(r["assessed_at"])).days <= 30
        ]
        
        if not recent_reports:
            return 30  # Outdated quality assessments
        
        # Calculate average quality score
        avg_score = sum(r["quality_score"] for r in recent_reports) / len(recent_reports)
        return avg_score
    
    def _check_lineage_compliance(self, system_id: str) -> float:
        """Check data lineage compliance for a system."""
        lineage_record = self.lineage_records.get(system_id)
        
        if not lineage_record:
            return 0  # No lineage tracking
        
        # Check if lineage is recent (within 60 days)
        lineage_date = datetime.fromisoformat(lineage_record["tracked_at"])
        if (datetime.utcnow() - lineage_date).days > 60:
            return 40  # Outdated lineage
        
        # Check completeness of lineage data
        data_flow = lineage_record.get("data_flow", [])
        transformations = lineage_record.get("transformations", [])
        
        completeness_score = 0
        if data_flow:
            completeness_score += 40
        if transformations:
            completeness_score += 30
        if lineage_record.get("dependencies"):
            completeness_score += 30
        
        return completeness_score
    
    def _check_privacy_compliance(self, system_id: str) -> float:
        """Check privacy compliance for a system."""
        compliance_records = self.compliance_records.get(system_id, [])
        
        if not compliance_records:
            return 0  # No privacy assessments
        
        # Get most recent compliance check
        latest_check = max(compliance_records, key=lambda x: x["checked_at"])
        return latest_check.get("overall_score", 0)
    
    def _check_retention_compliance(self, system_id: str) -> float:
        """Check data retention compliance for a system."""
        # Mock implementation - would check actual retention practices
        system_record = self.registered_systems[system_id]
        retention_policy = system_record.get("retention_policy", {})
        
        if retention_policy:
            return 85  # Good retention policy in place
        else:
            return 30  # No retention policy
    
    def _generate_data_recommendations(self, system_id: str, score: float) -> List[str]:
        """Generate data governance recommendations."""
        recommendations = []
        
        if score < 70:
            recommendations.append("Improve data governance compliance - score below threshold")
        
        # Check specific areas
        if not self.quality_reports.get(system_id):
            recommendations.append("Implement data quality monitoring")
        
        if not self.lineage_records.get(system_id):
            recommendations.append("Establish data lineage tracking")
        
        if not self.compliance_records.get(system_id):
            recommendations.append("Conduct privacy compliance assessment")
        
        return recommendations
    
    def _analyze_lineage_impact(self, lineage_data: Dict) -> Dict:
        """Analyze the impact of data lineage."""
        data_flow = lineage_data.get("data_flow", [])
        dependencies = lineage_data.get("dependencies", [])
        
        return {
            "upstream_systems": len(set(d.get("source_system", "") for d in data_flow)),
            "downstream_systems": len(set(d.get("target_system", "") for d in data_flow)),
            "critical_dependencies": len([d for d in dependencies if d.get("criticality") == "high"]),
            "impact_score": len(dependencies) * 10  # Simple impact calculation
        }
    
    def _check_gdpr_compliance(self, privacy_data: Dict) -> Dict:
        """Check GDPR compliance."""
        compliance = {
            "score": 0,
            "requirements_met": [],
            "requirements_missing": []
        }
        
        gdpr_requirements = [
            "lawful_basis",
            "data_subject_rights",
            "privacy_by_design",
            "data_protection_officer",
            "breach_notification"
        ]
        
        for requirement in gdpr_requirements:
            if privacy_data.get(requirement, False):
                compliance["requirements_met"].append(requirement)
                compliance["score"] += 20
            else:
                compliance["requirements_missing"].append(requirement)
        
        return compliance
    
    def _check_ccpa_compliance(self, privacy_data: Dict) -> Dict:
        """Check CCPA compliance."""
        compliance = {
            "score": 0,
            "requirements_met": [],
            "requirements_missing": []
        }
        
        ccpa_requirements = [
            "consumer_rights",
            "opt_out_mechanism",
            "privacy_notice",
            "data_sale_disclosure"
        ]
        
        for requirement in ccpa_requirements:
            if privacy_data.get(requirement, False):
                compliance["requirements_met"].append(requirement)
                compliance["score"] += 25
            else:
                compliance["requirements_missing"].append(requirement)
        
        return compliance
    
    def _check_data_minimization(self, privacy_data: Dict) -> Dict:
        """Check data minimization compliance."""
        return {
            "score": 80,  # Mock score
            "status": "compliant" if privacy_data.get("data_minimization", False) else "non_compliant"
        }
    
    def _check_consent_management(self, privacy_data: Dict) -> Dict:
        """Check consent management compliance."""
        return {
            "score": 75,  # Mock score
            "status": "compliant" if privacy_data.get("consent_management", False) else "non_compliant"
        }