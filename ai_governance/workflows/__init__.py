"""
Workflow Orchestration module for AI governance processes.

Implements workflow orchestration for governance processes, including
automated assessments, approval workflows, and integration with
existing business processes.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import json


class WorkflowStatus(Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowType(Enum):
    """Types of governance workflows."""
    SYSTEM_REGISTRATION = "system_registration"
    COMPLIANCE_ASSESSMENT = "compliance_assessment"
    MODEL_VALIDATION = "model_validation"
    RISK_ASSESSMENT = "risk_assessment"
    AUDIT_REVIEW = "audit_review"
    POLICY_UPDATE = "policy_update"


class WorkflowOrchestrator:
    """
    Orchestrates governance workflows and integrates with existing processes.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize the workflow orchestrator."""
        self.config = config or {}
        self.workflows: Dict[str, Dict] = {}
        self.workflow_templates: Dict[str, Dict] = {}
        self.active_workflows: Dict[str, Dict] = {}
        self.completed_workflows: Dict[str, Dict] = {}
        
        # Initialize workflow templates
        self._initialize_workflow_templates()
    
    def register_workflow_template(self, template_id: str, template_data: Dict):
        """
        Register a new workflow template.
        
        Args:
            template_id: Unique template identifier
            template_data: Template configuration
        """
        template = {
            "template_id": template_id,
            "name": template_data.get("name", template_id),
            "description": template_data.get("description", ""),
            "workflow_type": template_data.get("workflow_type", WorkflowType.COMPLIANCE_ASSESSMENT.value),
            "steps": template_data.get("steps", []),
            "triggers": template_data.get("triggers", []),
            "approvers": template_data.get("approvers", []),
            "notifications": template_data.get("notifications", []),
            "sla": template_data.get("sla", {}),
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.workflow_templates[template_id] = template
        return {"status": "registered", "template_id": template_id}
    
    def initiate_workflow(self, template_id: str, context: Dict) -> Dict:
        """
        Initiate a new workflow instance.
        
        Args:
            template_id: Template to use for the workflow
            context: Workflow execution context
            
        Returns:
            Workflow instance details
        """
        if template_id not in self.workflow_templates:
            return {"error": "Template not found"}
        
        template = self.workflow_templates[template_id]
        workflow_id = f"wf_{template_id}_{int(datetime.utcnow().timestamp())}"
        
        workflow_instance = {
            "workflow_id": workflow_id,
            "template_id": template_id,
            "workflow_type": template["workflow_type"],
            "status": WorkflowStatus.PENDING.value,
            "context": context,
            "steps": self._initialize_workflow_steps(template["steps"], context),
            "current_step": 0,
            "created_at": datetime.utcnow().isoformat(),
            "started_at": None,
            "completed_at": None,
            "approvals": [],
            "notifications_sent": [],
            "execution_log": [],
            "results": {}
        }
        
        self.workflows[workflow_id] = workflow_instance
        self.active_workflows[workflow_id] = workflow_instance
        
        # Auto-start if no manual trigger required
        if template.get("auto_start", True):
            self._execute_workflow(workflow_id)
        
        return {
            "status": "initiated",
            "workflow_id": workflow_id,
            "workflow_type": template["workflow_type"]
        }
    
    def execute_workflow_step(self, workflow_id: str, step_data: Dict = None) -> Dict:
        """
        Execute the next step in a workflow.
        
        Args:
            workflow_id: Workflow instance identifier
            step_data: Optional step-specific data
            
        Returns:
            Step execution results
        """
        if workflow_id not in self.workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.workflows[workflow_id]
        
        if workflow["status"] != WorkflowStatus.RUNNING.value:
            return {"error": "Workflow not in running state"}
        
        current_step_index = workflow["current_step"]
        steps = workflow["steps"]
        
        if current_step_index >= len(steps):
            return {"error": "No more steps to execute"}
        
        current_step = steps[current_step_index]
        
        # Execute step
        step_result = self._execute_step(workflow, current_step, step_data)
        
        # Log execution
        workflow["execution_log"].append({
            "step_index": current_step_index,
            "step_name": current_step["name"],
            "executed_at": datetime.utcnow().isoformat(),
            "result": step_result,
            "step_data": step_data
        })
        
        # Update workflow state
        if step_result["status"] == "completed":
            workflow["current_step"] += 1
            
            # Check if workflow is complete
            if workflow["current_step"] >= len(steps):
                self._complete_workflow(workflow_id)
        elif step_result["status"] == "failed":
            workflow["status"] = WorkflowStatus.FAILED.value
            workflow["completed_at"] = datetime.utcnow().isoformat()
            
            # Move to completed workflows
            self.completed_workflows[workflow_id] = workflow
            if workflow_id in self.active_workflows:
                del self.active_workflows[workflow_id]
        
        return step_result
    
    def approve_workflow_step(self, workflow_id: str, step_index: int, approver: str, decision: str, comments: str = "") -> Dict:
        """
        Approve or reject a workflow step.
        
        Args:
            workflow_id: Workflow instance identifier
            step_index: Index of the step to approve
            approver: Approver identifier
            decision: "approved" or "rejected"
            comments: Optional approval comments
            
        Returns:
            Approval result
        """
        if workflow_id not in self.workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.workflows[workflow_id]
        
        approval_record = {
            "workflow_id": workflow_id,
            "step_index": step_index,
            "approver": approver,
            "decision": decision,
            "comments": comments,
            "approved_at": datetime.utcnow().isoformat()
        }
        
        workflow["approvals"].append(approval_record)
        
        # Update step status
        if step_index < len(workflow["steps"]):
            step = workflow["steps"][step_index]
            if decision == "approved":
                step["approval_status"] = "approved"
                step["approved_by"] = approver
                step["approved_at"] = datetime.utcnow().isoformat()
            else:
                step["approval_status"] = "rejected"
                workflow["status"] = WorkflowStatus.FAILED.value
        
        return {"status": "recorded", "approval_id": f"approval_{int(datetime.utcnow().timestamp())}"}
    
    def get_workflow_status(self, workflow_id: str) -> Dict:
        """
        Get the current status of a workflow.
        
        Args:
            workflow_id: Workflow instance identifier
            
        Returns:
            Workflow status information
        """
        if workflow_id not in self.workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.workflows[workflow_id]
        
        # Calculate progress
        total_steps = len(workflow["steps"])
        completed_steps = workflow["current_step"]
        progress_percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0
        
        # Get pending approvals
        pending_approvals = []
        for i, step in enumerate(workflow["steps"]):
            if i >= workflow["current_step"] and step.get("requires_approval", False):
                if not step.get("approval_status"):
                    pending_approvals.append({
                        "step_index": i,
                        "step_name": step["name"],
                        "required_approvers": step.get("approvers", [])
                    })
        
        return {
            "workflow_id": workflow_id,
            "status": workflow["status"],
            "workflow_type": workflow["workflow_type"],
            "progress": {
                "total_steps": total_steps,
                "completed_steps": completed_steps,
                "current_step_name": workflow["steps"][workflow["current_step"]]["name"] if workflow["current_step"] < total_steps else "Completed",
                "progress_percentage": progress_percentage
            },
            "pending_approvals": pending_approvals,
            "created_at": workflow["created_at"],
            "started_at": workflow.get("started_at"),
            "completed_at": workflow.get("completed_at"),
            "execution_time": self._calculate_execution_time(workflow)
        }
    
    def list_workflows(self, status_filter: str = None, workflow_type_filter: str = None) -> Dict:
        """
        List workflows with optional filtering.
        
        Args:
            status_filter: Filter by workflow status
            workflow_type_filter: Filter by workflow type
            
        Returns:
            List of workflows
        """
        workflows = list(self.workflows.values())
        
        # Apply filters
        if status_filter:
            workflows = [w for w in workflows if w["status"] == status_filter]
        
        if workflow_type_filter:
            workflows = [w for w in workflows if w["workflow_type"] == workflow_type_filter]
        
        # Sort by creation date (most recent first)
        workflows.sort(key=lambda x: x["created_at"], reverse=True)
        
        # Summary statistics
        status_counts = {}
        type_counts = {}
        
        for workflow in workflows:
            status = workflow["status"]
            wf_type = workflow["workflow_type"]
            
            status_counts[status] = status_counts.get(status, 0) + 1
            type_counts[wf_type] = type_counts.get(wf_type, 0) + 1
        
        return {
            "total_workflows": len(workflows),
            "status_distribution": status_counts,
            "type_distribution": type_counts,
            "workflows": [
                {
                    "workflow_id": w["workflow_id"],
                    "workflow_type": w["workflow_type"],
                    "status": w["status"],
                    "created_at": w["created_at"],
                    "progress_percentage": (w["current_step"] / len(w["steps"]) * 100) if w["steps"] else 0
                }
                for w in workflows
            ]
        }
    
    def cancel_workflow(self, workflow_id: str, reason: str = "") -> Dict:
        """
        Cancel an active workflow.
        
        Args:
            workflow_id: Workflow instance identifier
            reason: Cancellation reason
            
        Returns:
            Cancellation result
        """
        if workflow_id not in self.workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.workflows[workflow_id]
        
        if workflow["status"] in [WorkflowStatus.COMPLETED.value, WorkflowStatus.FAILED.value, WorkflowStatus.CANCELLED.value]:
            return {"error": "Workflow cannot be cancelled in current state"}
        
        workflow["status"] = WorkflowStatus.CANCELLED.value
        workflow["completed_at"] = datetime.utcnow().isoformat()
        workflow["cancellation_reason"] = reason
        
        # Move to completed workflows
        self.completed_workflows[workflow_id] = workflow
        if workflow_id in self.active_workflows:
            del self.active_workflows[workflow_id]
        
        return {"status": "cancelled", "workflow_id": workflow_id}
    
    def _initialize_workflow_templates(self):
        """Initialize default workflow templates."""
        
        # System Registration Workflow
        self.workflow_templates["system_registration"] = {
            "template_id": "system_registration",
            "name": "AI System Registration",
            "description": "Complete registration process for new AI systems",
            "workflow_type": WorkflowType.SYSTEM_REGISTRATION.value,
            "steps": [
                {
                    "name": "Initial Registration",
                    "type": "automated",
                    "action": "register_system",
                    "requires_approval": False
                },
                {
                    "name": "Risk Assessment",
                    "type": "automated",
                    "action": "assess_risk",
                    "requires_approval": False
                },
                {
                    "name": "Governance Level Assignment",
                    "type": "automated",
                    "action": "assign_governance_level",
                    "requires_approval": False
                },
                {
                    "name": "Management Review",
                    "type": "manual",
                    "action": "management_review",
                    "requires_approval": True,
                    "approvers": ["ai_governance_manager", "risk_manager"]
                },
                {
                    "name": "Final Approval",
                    "type": "manual",
                    "action": "final_approval",
                    "requires_approval": True,
                    "approvers": ["chief_risk_officer"]
                }
            ],
            "auto_start": True
        }
        
        # Compliance Assessment Workflow
        self.workflow_templates["compliance_assessment"] = {
            "template_id": "compliance_assessment",
            "name": "Compliance Assessment",
            "description": "Comprehensive compliance assessment for AI systems",
            "workflow_type": WorkflowType.COMPLIANCE_ASSESSMENT.value,
            "steps": [
                {
                    "name": "Model Risk Assessment",
                    "type": "automated",
                    "action": "assess_model_risk",
                    "requires_approval": False
                },
                {
                    "name": "AI Oversight Assessment",
                    "type": "automated",
                    "action": "assess_ai_oversight",
                    "requires_approval": False
                },
                {
                    "name": "Data Governance Assessment",
                    "type": "automated",
                    "action": "assess_data_governance",
                    "requires_approval": False
                },
                {
                    "name": "Data Residency Assessment",
                    "type": "automated",
                    "action": "assess_data_residency",
                    "requires_approval": False
                },
                {
                    "name": "ISO Compliance Assessment",
                    "type": "automated",
                    "action": "assess_iso_compliance",
                    "requires_approval": False
                },
                {
                    "name": "Generate Compliance Report",
                    "type": "automated",
                    "action": "generate_report",
                    "requires_approval": False
                },
                {
                    "name": "Compliance Review",
                    "type": "manual",
                    "action": "compliance_review",
                    "requires_approval": True,
                    "approvers": ["compliance_officer", "ai_governance_manager"]
                }
            ],
            "auto_start": True
        }
    
    def _initialize_workflow_steps(self, template_steps: List[Dict], context: Dict) -> List[Dict]:
        """Initialize workflow steps with context."""
        steps = []
        
        for step in template_steps:
            initialized_step = step.copy()
            initialized_step["status"] = "pending"
            initialized_step["started_at"] = None
            initialized_step["completed_at"] = None
            initialized_step["result"] = None
            steps.append(initialized_step)
        
        return steps
    
    def _execute_workflow(self, workflow_id: str):
        """Start workflow execution."""
        workflow = self.workflows[workflow_id]
        workflow["status"] = WorkflowStatus.RUNNING.value
        workflow["started_at"] = datetime.utcnow().isoformat()
        
        # Execute first step if it's automated
        if workflow["steps"] and workflow["steps"][0].get("type") == "automated":
            self.execute_workflow_step(workflow_id)
    
    def _execute_step(self, workflow: Dict, step: Dict, step_data: Dict = None) -> Dict:
        """Execute a single workflow step."""
        step["started_at"] = datetime.utcnow().isoformat()
        step["status"] = "running"
        
        try:
            if step["type"] == "automated":
                result = self._execute_automated_step(workflow, step, step_data)
            else:
                result = self._execute_manual_step(workflow, step, step_data)
            
            step["status"] = "completed"
            step["completed_at"] = datetime.utcnow().isoformat()
            step["result"] = result
            
            return {"status": "completed", "result": result}
            
        except Exception as e:
            step["status"] = "failed"
            step["completed_at"] = datetime.utcnow().isoformat()
            step["error"] = str(e)
            
            return {"status": "failed", "error": str(e)}
    
    def _execute_automated_step(self, workflow: Dict, step: Dict, step_data: Dict = None) -> Dict:
        """Execute an automated workflow step."""
        action = step.get("action", "")
        context = workflow.get("context", {})
        
        # Mock automated step execution
        # In practice, this would integrate with actual governance modules
        
        if action == "register_system":
            return {
                "action": "register_system",
                "system_id": context.get("system_id", "unknown"),
                "status": "registered",
                "governance_level": "medium"
            }
        elif action == "assess_risk":
            return {
                "action": "assess_risk",
                "risk_level": "medium",
                "risk_score": 75,
                "risk_factors": ["data_sensitivity", "model_complexity"]
            }
        elif action == "assess_model_risk":
            return {
                "action": "assess_model_risk",
                "score": 80,
                "status": "compliant"
            }
        elif action == "assess_ai_oversight":
            return {
                "action": "assess_ai_oversight",
                "score": 85,
                "status": "compliant"
            }
        elif action == "assess_data_governance":
            return {
                "action": "assess_data_governance",
                "score": 78,
                "status": "compliant"
            }
        elif action == "assess_data_residency":
            return {
                "action": "assess_data_residency",
                "score": 82,
                "status": "compliant"
            }
        elif action == "assess_iso_compliance":
            return {
                "action": "assess_iso_compliance",
                "score": 79,
                "status": "compliant"
            }
        elif action == "generate_report":
            return {
                "action": "generate_report",
                "report_id": f"report_{int(datetime.utcnow().timestamp())}",
                "status": "generated"
            }
        else:
            return {
                "action": action,
                "status": "completed",
                "message": f"Automated step {action} executed successfully"
            }
    
    def _execute_manual_step(self, workflow: Dict, step: Dict, step_data: Dict = None) -> Dict:
        """Execute a manual workflow step."""
        # Manual steps require human intervention
        if step.get("requires_approval", False):
            return {
                "status": "pending_approval",
                "message": "Step requires manual approval",
                "required_approvers": step.get("approvers", [])
            }
        else:
            return {
                "status": "pending_manual_action",
                "message": "Step requires manual execution"
            }
    
    def _complete_workflow(self, workflow_id: str):
        """Complete a workflow."""
        workflow = self.workflows[workflow_id]
        workflow["status"] = WorkflowStatus.COMPLETED.value
        workflow["completed_at"] = datetime.utcnow().isoformat()
        
        # Compile final results
        workflow["results"] = self._compile_workflow_results(workflow)
        
        # Move to completed workflows
        self.completed_workflows[workflow_id] = workflow
        if workflow_id in self.active_workflows:
            del self.active_workflows[workflow_id]
    
    def _compile_workflow_results(self, workflow: Dict) -> Dict:
        """Compile final results from workflow execution."""
        results = {
            "workflow_id": workflow["workflow_id"],
            "workflow_type": workflow["workflow_type"],
            "execution_summary": {
                "total_steps": len(workflow["steps"]),
                "successful_steps": len([s for s in workflow["steps"] if s.get("status") == "completed"]),
                "failed_steps": len([s for s in workflow["steps"] if s.get("status") == "failed"])
            },
            "step_results": [],
            "final_status": workflow["status"],
            "execution_time": self._calculate_execution_time(workflow)
        }
        
        # Collect results from each step
        for step in workflow["steps"]:
            if step.get("result"):
                results["step_results"].append({
                    "step_name": step["name"],
                    "result": step["result"]
                })
        
        return results
    
    def _calculate_execution_time(self, workflow: Dict) -> Dict:
        """Calculate workflow execution time."""
        started_at = workflow.get("started_at")
        completed_at = workflow.get("completed_at")
        
        if not started_at:
            return {"status": "not_started"}
        
        start_time = datetime.fromisoformat(started_at)
        
        if completed_at:
            end_time = datetime.fromisoformat(completed_at)
            duration = end_time - start_time
        else:
            duration = datetime.utcnow() - start_time
        
        return {
            "started_at": started_at,
            "completed_at": completed_at,
            "duration_seconds": duration.total_seconds(),
            "duration_human": str(duration)
        }