"""
Data Residency module for managing data location compliance.

Implements data residency management for cloud environments, ensuring
compliance with regulatory requirements and organizational policies
regarding data location and sovereignty.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import json


class DataSovereigntyLevel(Enum):
    """Data sovereignty requirements levels."""
    NONE = "none"
    BASIC = "basic"
    STRICT = "strict"
    ABSOLUTE = "absolute"


class ComplianceStatus(Enum):
    """Compliance status levels."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    UNDER_REVIEW = "under_review"
    UNKNOWN = "unknown"


class DataResidencyManager:
    """
    Manages data residency and sovereignty compliance for AI systems.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize the data residency manager."""
        self.config = config or {}
        self.registered_systems: Dict[str, Dict] = {}
        self.residency_policies: Dict[str, Dict] = {}
        self.compliance_assessments: Dict[str, List] = {}
        self.data_locations: Dict[str, Dict] = {}
        
        # Initialize default policies
        self._initialize_default_policies()
        
    def register_system(self, system_id: str, system_info: Dict):
        """Register a system for data residency management."""
        residency_record = {
            "system_id": system_id,
            "system_name": system_info.get("name", system_id),
            "jurisdictions": system_info.get("jurisdictions", []),
            "data_types": system_info.get("data_types", []),
            "cloud_provider": system_info.get("cloud_provider", "unknown"),
            "sovereignty_level": self._determine_sovereignty_level(system_info),
            "registered_at": datetime.utcnow().isoformat(),
            "residency_requirements": self._get_residency_requirements(system_info),
            "approved_regions": self._get_approved_regions(system_info),
            "restricted_regions": self._get_restricted_regions(system_info)
        }
        
        self.registered_systems[system_id] = residency_record
        self.compliance_assessments[system_id] = []
        
        # Initialize data location tracking
        self._initialize_data_location_tracking(system_id, system_info)
        
    def assess_residency_compliance(self, system_id: str) -> Dict:
        """
        Assess data residency compliance for a registered system.
        
        Args:
            system_id: System identifier
            
        Returns:
            Data residency compliance assessment
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered", "score": 0}
        
        system_record = self.registered_systems[system_id]
        
        # Check various compliance aspects
        location_compliance = self._check_location_compliance(system_id)
        sovereignty_compliance = self._check_sovereignty_compliance(system_id)
        transfer_compliance = self._check_transfer_compliance(system_id)
        policy_compliance = self._check_policy_compliance(system_id)
        
        # Calculate overall compliance score
        overall_score = (
            location_compliance * 0.3 +
            sovereignty_compliance * 0.3 +
            transfer_compliance * 0.25 +
            policy_compliance * 0.15
        )
        
        assessment = {
            "system_id": system_id,
            "assessed_at": datetime.utcnow().isoformat(),
            "sovereignty_level": system_record["sovereignty_level"],
            "score": overall_score,
            "compliance_areas": {
                "location_compliance": location_compliance,
                "sovereignty_compliance": sovereignty_compliance,
                "transfer_compliance": transfer_compliance,
                "policy_compliance": policy_compliance
            },
            "current_locations": self._get_current_data_locations(system_id),
            "violations": self._identify_violations(system_id),
            "recommendations": self._generate_residency_recommendations(system_id, overall_score),
            "next_review_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
        }
        
        # Store assessment
        self.compliance_assessments[system_id].append(assessment)
        
        return assessment
    
    def track_data_location(self, system_id: str, location_data: Dict):
        """
        Track data location for a system.
        
        Args:
            system_id: System identifier
            location_data: Data location information
        """
        if system_id not in self.registered_systems:
            return {"error": "System not registered"}
        
        location_record = {
            "system_id": system_id,
            "tracked_at": datetime.utcnow().isoformat(),
            "data_stores": location_data.get("data_stores", []),
            "processing_locations": location_data.get("processing_locations", []),
            "backup_locations": location_data.get("backup_locations", []),
            "transit_paths": location_data.get("transit_paths", []),
            "compliance_status": self._evaluate_location_compliance(system_id, location_data)
        }
        
        self.data_locations[system_id] = location_record
        
        # Check for immediate violations
        violations = self._check_immediate_violations(system_id, location_data)
        if violations:
            self._trigger_violation_alerts(system_id, violations)
        
        return {"status": "tracked", "violations": violations}
    
    def update_residency_policy(self, policy_id: str, policy_data: Dict):
        """
        Update or create a data residency policy.
        
        Args:
            policy_id: Policy identifier
            policy_data: Policy configuration
        """
        policy = {
            "policy_id": policy_id,
            "name": policy_data.get("name", policy_id),
            "updated_at": datetime.utcnow().isoformat(),
            "scope": policy_data.get("scope", []),
            "allowed_regions": policy_data.get("allowed_regions", []),
            "restricted_regions": policy_data.get("restricted_regions", []),
            "data_types": policy_data.get("data_types", []),
            "transfer_requirements": policy_data.get("transfer_requirements", {}),
            "sovereignty_requirements": policy_data.get("sovereignty_requirements", {}),
            "exceptions": policy_data.get("exceptions", [])
        }
        
        self.residency_policies[policy_id] = policy
        return {"status": "updated", "policy_id": policy_id}
    
    def get_residency_report(self, system_id: str = None) -> Dict:
        """
        Generate comprehensive data residency report.
        
        Args:
            system_id: Optional system identifier to filter by
            
        Returns:
            Data residency report
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
            "compliant_systems": 0,
            "non_compliant_systems": 0,
            "under_review_systems": 0
        }
        
        system_details = []
        
        for sid, system_record in systems.items():
            # Get latest assessment
            assessments = self.compliance_assessments.get(sid, [])
            latest_assessment = assessments[-1] if assessments else None
            
            if latest_assessment:
                score = latest_assessment["score"]
                if score >= 90:
                    compliance_summary["compliant_systems"] += 1
                    status = ComplianceStatus.COMPLIANT.value
                elif score >= 70:
                    compliance_summary["under_review_systems"] += 1
                    status = ComplianceStatus.UNDER_REVIEW.value
                else:
                    compliance_summary["non_compliant_systems"] += 1
                    status = ComplianceStatus.NON_COMPLIANT.value
            else:
                status = ComplianceStatus.UNKNOWN.value
            
            system_details.append({
                "system_id": sid,
                "system_name": system_record["system_name"],
                "sovereignty_level": system_record["sovereignty_level"],
                "compliance_status": status,
                "latest_score": latest_assessment["score"] if latest_assessment else None,
                "violations": latest_assessment.get("violations", []) if latest_assessment else []
            })
        
        # Regional distribution
        regional_distribution = self._analyze_regional_distribution(systems)
        
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "scope": f"system_{system_id}" if system_id else "all_systems",
            "compliance_summary": compliance_summary,
            "regional_distribution": regional_distribution,
            "system_details": system_details,
            "policy_summary": {
                "total_policies": len(self.residency_policies),
                "active_policies": len([p for p in self.residency_policies.values() if p.get("active", True)])
            }
        }
        
        return report
    
    def validate_data_transfer(self, from_region: str, to_region: str, data_types: List[str], system_id: str = None) -> Dict:
        """
        Validate if a data transfer is compliant with residency policies.
        
        Args:
            from_region: Source region
            to_region: Destination region
            data_types: Types of data being transferred
            system_id: Optional system identifier for specific policies
            
        Returns:
            Transfer validation results
        """
        validation = {
            "transfer_id": f"transfer_{int(datetime.utcnow().timestamp())}",
            "from_region": from_region,
            "to_region": to_region,
            "data_types": data_types,
            "validated_at": datetime.utcnow().isoformat(),
            "is_compliant": True,
            "violations": [],
            "requirements": [],
            "recommendations": []
        }
        
        # Check against applicable policies
        applicable_policies = self._get_applicable_policies(data_types, system_id)
        
        for policy in applicable_policies:
            policy_validation = self._validate_against_policy(from_region, to_region, data_types, policy)
            
            if not policy_validation["compliant"]:
                validation["is_compliant"] = False
                validation["violations"].extend(policy_validation["violations"])
            
            validation["requirements"].extend(policy_validation["requirements"])
        
        # Add transfer requirements based on regions
        transfer_requirements = self._get_transfer_requirements(from_region, to_region, data_types)
        validation["requirements"].extend(transfer_requirements)
        
        # Generate recommendations
        if not validation["is_compliant"]:
            validation["recommendations"] = self._generate_transfer_recommendations(validation)
        
        return validation
    
    def _determine_sovereignty_level(self, system_info: Dict) -> str:
        """Determine data sovereignty level requirements."""
        data_types = system_info.get("data_types", [])
        jurisdictions = system_info.get("jurisdictions", [])
        use_case = system_info.get("use_case", "").lower()
        
        # Check for highly sensitive data
        if any(dtype.lower() in ["government", "defense", "critical_infrastructure"] for dtype in data_types):
            return DataSovereigntyLevel.ABSOLUTE.value
        
        # Check jurisdictions with strict requirements
        strict_jurisdictions = ["russia", "china", "iran"]
        if any(j.lower() in strict_jurisdictions for j in jurisdictions):
            return DataSovereigntyLevel.STRICT.value
        
        # Check for regulated industries
        if any(case in use_case for case in ["banking", "healthcare", "government"]):
            return DataSovereigntyLevel.STRICT.value
        
        # Check for personal data
        if "pii" in [dtype.lower() for dtype in data_types]:
            return DataSovereigntyLevel.BASIC.value
        
        return DataSovereigntyLevel.NONE.value
    
    def _get_residency_requirements(self, system_info: Dict) -> List[str]:
        """Get data residency requirements based on system information."""
        sovereignty_level = self._determine_sovereignty_level(system_info)
        jurisdictions = system_info.get("jurisdictions", [])
        
        requirements = ["location_tracking", "compliance_monitoring"]
        
        if sovereignty_level in [DataSovereigntyLevel.BASIC.value, DataSovereigntyLevel.STRICT.value, DataSovereigntyLevel.ABSOLUTE.value]:
            requirements.extend([
                "approved_regions_only",
                "transfer_controls",
                "audit_logging"
            ])
        
        if sovereignty_level in [DataSovereigntyLevel.STRICT.value, DataSovereigntyLevel.ABSOLUTE.value]:
            requirements.extend([
                "real_time_monitoring",
                "immediate_violation_alerts",
                "encryption_requirements"
            ])
        
        if sovereignty_level == DataSovereigntyLevel.ABSOLUTE.value:
            requirements.extend([
                "no_cross_border_transfers",
                "government_approval_required",
                "local_processing_only"
            ])
        
        # Jurisdiction-specific requirements
        if "eu" in [j.lower() for j in jurisdictions]:
            requirements.append("gdpr_adequate_countries_only")
        
        return requirements
    
    def _get_approved_regions(self, system_info: Dict) -> List[str]:
        """Get approved regions based on system information."""
        jurisdictions = system_info.get("jurisdictions", [])
        sovereignty_level = self._determine_sovereignty_level(system_info)
        
        # Default approved regions
        approved_regions = ["us-east-1", "us-west-2", "eu-west-1"]
        
        # Adjust based on sovereignty level
        if sovereignty_level == DataSovereigntyLevel.ABSOLUTE.value:
            # Only local regions
            if "us" in [j.lower() for j in jurisdictions]:
                approved_regions = ["us-east-1", "us-west-2"]
            elif "eu" in [j.lower() for j in jurisdictions]:
                approved_regions = ["eu-west-1", "eu-central-1"]
        
        return approved_regions
    
    def _get_restricted_regions(self, system_info: Dict) -> List[str]:
        """Get restricted regions based on system information."""
        sovereignty_level = self._determine_sovereignty_level(system_info)
        
        # Default restricted regions
        restricted_regions = []
        
        if sovereignty_level in [DataSovereigntyLevel.STRICT.value, DataSovereigntyLevel.ABSOLUTE.value]:
            restricted_regions.extend([
                "cn-north-1",  # China
                "ap-south-1",  # India (if not specifically approved)
                "me-south-1"   # Middle East
            ])
        
        return restricted_regions
    
    def _initialize_default_policies(self):
        """Initialize default data residency policies."""
        # EU GDPR Policy
        self.residency_policies["gdpr_policy"] = {
            "policy_id": "gdpr_policy",
            "name": "GDPR Data Residency Policy",
            "scope": ["eu"],
            "allowed_regions": ["eu-west-1", "eu-central-1", "eu-north-1"],
            "restricted_regions": ["cn-north-1", "ap-south-1"],
            "data_types": ["pii", "personal_data"],
            "transfer_requirements": {
                "adequacy_decision_required": True,
                "safeguards_required": True
            },
            "active": True
        }
        
        # US Financial Services Policy
        self.residency_policies["us_financial_policy"] = {
            "policy_id": "us_financial_policy",
            "name": "US Financial Services Data Policy",
            "scope": ["us", "financial"],
            "allowed_regions": ["us-east-1", "us-west-2"],
            "restricted_regions": ["cn-north-1"],
            "data_types": ["financial", "pii"],
            "transfer_requirements": {
                "regulatory_approval_required": True,
                "encryption_required": True
            },
            "active": True
        }
    
    def _initialize_data_location_tracking(self, system_id: str, system_info: Dict):
        """Initialize data location tracking for a system."""
        # Mock initial location data
        initial_locations = {
            "system_id": system_id,
            "tracked_at": datetime.utcnow().isoformat(),
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
        
        self.data_locations[system_id] = initial_locations
    
    def _check_location_compliance(self, system_id: str) -> float:
        """Check location compliance for a system."""
        system_record = self.registered_systems[system_id]
        location_data = self.data_locations.get(system_id, {})
        
        approved_regions = system_record["approved_regions"]
        restricted_regions = system_record["restricted_regions"]
        
        if not location_data:
            return 0  # No location data
        
        violations = 0
        total_locations = 0
        
        # Check data stores
        for store in location_data.get("data_stores", []):
            total_locations += 1
            region = store.get("region", "")
            if region in restricted_regions or (approved_regions and region not in approved_regions):
                violations += 1
        
        # Check processing locations
        for proc in location_data.get("processing_locations", []):
            total_locations += 1
            region = proc.get("region", "")
            if region in restricted_regions or (approved_regions and region not in approved_regions):
                violations += 1
        
        if total_locations == 0:
            return 50  # No location data available
        
        compliance_rate = (total_locations - violations) / total_locations
        return compliance_rate * 100
    
    def _check_sovereignty_compliance(self, system_id: str) -> float:
        """Check data sovereignty compliance for a system."""
        system_record = self.registered_systems[system_id]
        sovereignty_level = system_record["sovereignty_level"]
        
        # Mock sovereignty compliance check
        if sovereignty_level == DataSovereigntyLevel.ABSOLUTE.value:
            return 90  # Strict compliance required
        elif sovereignty_level == DataSovereigntyLevel.STRICT.value:
            return 85
        elif sovereignty_level == DataSovereigntyLevel.BASIC.value:
            return 80
        else:
            return 95  # No sovereignty requirements
    
    def _check_transfer_compliance(self, system_id: str) -> float:
        """Check data transfer compliance for a system."""
        # Mock transfer compliance check
        return 85  # Assume good transfer compliance
    
    def _check_policy_compliance(self, system_id: str) -> float:
        """Check policy compliance for a system."""
        system_record = self.registered_systems[system_id]
        data_types = system_record["data_types"]
        
        # Check applicable policies
        applicable_policies = self._get_applicable_policies(data_types, system_id)
        
        if not applicable_policies:
            return 90  # No applicable policies
        
        # Mock policy compliance score
        return 80
    
    def _get_current_data_locations(self, system_id: str) -> Dict:
        """Get current data locations for a system."""
        return self.data_locations.get(system_id, {})
    
    def _identify_violations(self, system_id: str) -> List[Dict]:
        """Identify compliance violations for a system."""
        violations = []
        
        system_record = self.registered_systems[system_id]
        location_data = self.data_locations.get(system_id, {})
        
        approved_regions = system_record["approved_regions"]
        restricted_regions = system_record["restricted_regions"]
        
        # Check for restricted region usage
        for store in location_data.get("data_stores", []):
            region = store.get("region", "")
            if region in restricted_regions:
                violations.append({
                    "type": "restricted_region_usage",
                    "description": f"Data stored in restricted region: {region}",
                    "severity": "high",
                    "resource": store
                })
        
        # Check for unapproved region usage
        if approved_regions:
            for store in location_data.get("data_stores", []):
                region = store.get("region", "")
                if region not in approved_regions:
                    violations.append({
                        "type": "unapproved_region_usage",
                        "description": f"Data stored in unapproved region: {region}",
                        "severity": "medium",
                        "resource": store
                    })
        
        return violations
    
    def _generate_residency_recommendations(self, system_id: str, score: float) -> List[str]:
        """Generate data residency recommendations."""
        recommendations = []
        
        if score < 80:
            recommendations.append("Improve data residency compliance - score below threshold")
        
        violations = self._identify_violations(system_id)
        if violations:
            recommendations.append(f"Address {len(violations)} compliance violations")
        
        # Check location tracking
        if system_id not in self.data_locations:
            recommendations.append("Implement data location tracking")
        
        return recommendations
    
    def _evaluate_location_compliance(self, system_id: str, location_data: Dict) -> str:
        """Evaluate location compliance status."""
        violations = self._check_immediate_violations(system_id, location_data)
        
        if not violations:
            return ComplianceStatus.COMPLIANT.value
        
        # Check severity of violations
        high_severity = [v for v in violations if v.get("severity") == "high"]
        if high_severity:
            return ComplianceStatus.NON_COMPLIANT.value
        
        return ComplianceStatus.UNDER_REVIEW.value
    
    def _check_immediate_violations(self, system_id: str, location_data: Dict) -> List[Dict]:
        """Check for immediate compliance violations."""
        system_record = self.registered_systems[system_id]
        restricted_regions = system_record["restricted_regions"]
        
        violations = []
        
        # Check all location types
        for location_type in ["data_stores", "processing_locations", "backup_locations"]:
            for location in location_data.get(location_type, []):
                region = location.get("region", "")
                if region in restricted_regions:
                    violations.append({
                        "type": "restricted_region_violation",
                        "location_type": location_type,
                        "region": region,
                        "severity": "high"
                    })
        
        return violations
    
    def _trigger_violation_alerts(self, system_id: str, violations: List[Dict]):
        """Trigger alerts for compliance violations."""
        # Mock alert system - would integrate with actual alerting
        for violation in violations:
            if violation.get("severity") == "high":
                print(f"CRITICAL ALERT: Data residency violation in system {system_id}: {violation}")
    
    def _analyze_regional_distribution(self, systems: Dict) -> Dict:
        """Analyze regional distribution of systems."""
        region_counts = {}
        
        for system_id, system_record in systems.items():
            location_data = self.data_locations.get(system_id, {})
            
            for store in location_data.get("data_stores", []):
                region = store.get("region", "unknown")
                region_counts[region] = region_counts.get(region, 0) + 1
        
        return region_counts
    
    def _get_applicable_policies(self, data_types: List[str], system_id: str = None) -> List[Dict]:
        """Get policies applicable to given data types and system."""
        applicable_policies = []
        
        for policy in self.residency_policies.values():
            if not policy.get("active", True):
                continue
            
            # Check if policy applies to data types
            policy_data_types = policy.get("data_types", [])
            if any(dtype in policy_data_types for dtype in data_types):
                applicable_policies.append(policy)
        
        return applicable_policies
    
    def _validate_against_policy(self, from_region: str, to_region: str, data_types: List[str], policy: Dict) -> Dict:
        """Validate transfer against a specific policy."""
        validation = {
            "policy_id": policy["policy_id"],
            "compliant": True,
            "violations": [],
            "requirements": []
        }
        
        allowed_regions = policy.get("allowed_regions", [])
        restricted_regions = policy.get("restricted_regions", [])
        
        # Check source region
        if allowed_regions and from_region not in allowed_regions:
            validation["compliant"] = False
            validation["violations"].append(f"Source region {from_region} not in allowed regions")
        
        if from_region in restricted_regions:
            validation["compliant"] = False
            validation["violations"].append(f"Source region {from_region} is restricted")
        
        # Check destination region
        if allowed_regions and to_region not in allowed_regions:
            validation["compliant"] = False
            validation["violations"].append(f"Destination region {to_region} not in allowed regions")
        
        if to_region in restricted_regions:
            validation["compliant"] = False
            validation["violations"].append(f"Destination region {to_region} is restricted")
        
        # Add transfer requirements
        transfer_requirements = policy.get("transfer_requirements", {})
        for requirement, required in transfer_requirements.items():
            if required:
                validation["requirements"].append(requirement)
        
        return validation
    
    def _get_transfer_requirements(self, from_region: str, to_region: str, data_types: List[str]) -> List[str]:
        """Get transfer requirements based on regions and data types."""
        requirements = []
        
        # Cross-border transfer requirements
        if self._is_cross_border_transfer(from_region, to_region):
            requirements.append("cross_border_transfer_approval")
            
            if "pii" in data_types:
                requirements.append("data_protection_safeguards")
        
        # Encryption requirements for sensitive data
        if any(dtype in ["pii", "financial", "health"] for dtype in data_types):
            requirements.append("encryption_in_transit")
            requirements.append("encryption_at_rest")
        
        return requirements
    
    def _is_cross_border_transfer(self, from_region: str, to_region: str) -> bool:
        """Check if transfer is cross-border."""
        # Simple check based on region prefixes
        from_country = from_region.split("-")[0]
        to_country = to_region.split("-")[0]
        
        return from_country != to_country
    
    def _generate_transfer_recommendations(self, validation: Dict) -> List[str]:
        """Generate recommendations for non-compliant transfers."""
        recommendations = []
        
        violations = validation.get("violations", [])
        
        if any("restricted" in v for v in violations):
            recommendations.append("Use alternative regions that are not restricted")
        
        if any("not in allowed" in v for v in violations):
            recommendations.append("Transfer data to approved regions only")
        
        requirements = validation.get("requirements", [])
        if "cross_border_transfer_approval" in requirements:
            recommendations.append("Obtain regulatory approval for cross-border transfer")
        
        if "encryption_in_transit" in requirements:
            recommendations.append("Implement encryption for data in transit")
        
        return recommendations