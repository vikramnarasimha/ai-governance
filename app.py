"""
FastAPI application for AI Governance platform.

Provides REST API endpoints for AI governance functionality including
system registration, compliance assessments, and reporting.
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os

from ai_governance import GovernanceFramework, WorkflowOrchestrator


# Pydantic models for API requests/responses
class SystemRegistrationRequest(BaseModel):
    system_id: str = Field(..., description="Unique system identifier")
    name: str = Field(..., description="System name")
    description: str = Field("", description="System description")
    use_case: str = Field(..., description="AI use case")
    model_type: str = Field("", description="Type of AI model")
    data_sources: List[str] = Field(default_factory=list, description="Data sources")
    data_types: List[str] = Field(default_factory=list, description="Types of data")
    data_sensitivity: str = Field("medium", description="Data sensitivity level")
    risk_factors: List[str] = Field(default_factory=list, description="Risk factors")
    jurisdictions: List[str] = Field(default_factory=list, description="Operating jurisdictions")
    cloud_provider: str = Field("", description="Cloud provider")
    industry_sector: str = Field("", description="Industry sector")


class ComplianceAssessmentResponse(BaseModel):
    system_id: str
    overall_score: float
    compliance_status: str
    module_assessments: Dict[str, Any]
    recommendations: List[str]
    assessed_at: str


class WorkflowInitiationRequest(BaseModel):
    template_id: str = Field(..., description="Workflow template ID")
    system_id: str = Field(..., description="System ID for workflow context")
    additional_context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


# Initialize FastAPI app
app = FastAPI(
    title="AI Governance Platform",
    description="Comprehensive AI governance solution for Financial Services Institutions",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize governance framework and workflow orchestrator
governance_framework = GovernanceFramework()
workflow_orchestrator = WorkflowOrchestrator()


# Dependency to get governance framework
def get_governance_framework() -> GovernanceFramework:
    return governance_framework


def get_workflow_orchestrator() -> WorkflowOrchestrator:
    return workflow_orchestrator


# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main dashboard page."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Governance Platform</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .card { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .btn { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
            .btn:hover { background: #2980b9; }
            .metric { text-align: center; padding: 20px; }
            .metric h3 { margin: 0; font-size: 2em; color: #3498db; }
            .metric p { margin: 5px 0 0 0; color: #666; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
            .menu { background: #34495e; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
            .menu a { color: white; text-decoration: none; margin-right: 20px; padding: 8px 16px; border-radius: 4px; }
            .menu a:hover { background: #2c3e50; }
            pre { background: #f8f9fa; padding: 15px; border-radius: 4px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI Governance Platform</h1>
                <p>Comprehensive AI governance solution for Financial Services Institutions</p>
            </div>
            
            <div class="menu">
                <a href="/api/docs" target="_blank">📖 API Documentation</a>
                <a href="/dashboard">📊 Dashboard</a>
                <a href="/systems">🏢 Systems</a>
                <a href="/workflows">⚙️ Workflows</a>
                <a href="/reports">📋 Reports</a>
            </div>
            
            <div class="grid">
                <div class="card">
                    <h3>🏢 System Registration</h3>
                    <p>Register and manage AI systems for governance oversight.</p>
                    <a href="/api/docs#/Systems/register_system_api_systems_register_post" class="btn" target="_blank">Register System</a>
                </div>
                
                <div class="card">
                    <h3>🔍 Compliance Assessment</h3>
                    <p>Comprehensive compliance assessment across all governance modules.</p>
                    <a href="/api/docs#/Compliance/assess_system_compliance_api_compliance_assess__system_id__post" class="btn" target="_blank">Run Assessment</a>
                </div>
                
                <div class="card">
                    <h3>⚙️ Workflow Management</h3>
                    <p>Orchestrate governance workflows and approval processes.</p>
                    <a href="/api/docs#/Workflows/initiate_workflow_api_workflows_initiate_post" class="btn" target="_blank">Start Workflow</a>
                </div>
                
                <div class="card">
                    <h3>📊 Governance Dashboard</h3>
                    <p>Monitor compliance status and governance metrics.</p>
                    <a href="/dashboard" class="btn">View Dashboard</a>
                </div>
            </div>
            
            <div class="card">
                <h3>📋 Key Features</h3>
                <ul>
                    <li><strong>Model Risk Management:</strong> Comprehensive model validation, performance monitoring, and risk assessment</li>
                    <li><strong>AI Oversight:</strong> Decision logging, transparency reporting, and escalation procedures</li>
                    <li><strong>Data Governance:</strong> Data quality monitoring, lineage tracking, and privacy compliance</li>
                    <li><strong>Data Residency:</strong> Location compliance monitoring and cross-border transfer validation</li>
                    <li><strong>ISO Standards:</strong> Compliance with ISO/IEC 23053, 23901, and other relevant standards</li>
                    <li><strong>Workflow Orchestration:</strong> Automated governance processes and approval workflows</li>
                </ul>
            </div>
            
            <div class="card">
                <h3>🚀 Quick Start</h3>
                <p>Get started with the AI Governance Platform:</p>
                <ol>
                    <li>Register your AI system using the registration endpoint</li>
                    <li>Run a compliance assessment to understand current status</li>
                    <li>Review recommendations and initiate improvement workflows</li>
                    <li>Monitor progress through the dashboard</li>
                </ol>
                <p><a href="/api/docs" class="btn" target="_blank">Explore API Documentation</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# Dashboard endpoint
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(governance: GovernanceFramework = Depends(get_governance_framework)):
    """Serve the governance dashboard."""
    dashboard_data = governance.get_governance_dashboard()
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Governance Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
            .card {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .metric {{ text-align: center; padding: 20px; }}
            .metric h3 {{ margin: 0; font-size: 2em; color: #3498db; }}
            .metric p {{ margin: 5px 0 0 0; color: #666; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }}
            .status-good {{ color: #27ae60; }}
            .status-warning {{ color: #f39c12; }}
            .status-critical {{ color: #e74c3c; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f8f9fa; }}
            .btn {{ background: #3498db; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 AI Governance Dashboard</h1>
                <p>Real-time governance compliance monitoring</p>
                <a href="/" class="btn">← Back to Home</a>
            </div>
            
            <div class="grid">
                <div class="card">
                    <div class="metric">
                        <h3>{dashboard_data['summary']['total_systems']}</h3>
                        <p>Total AI Systems</p>
                    </div>
                </div>
                
                <div class="card">
                    <div class="metric">
                        <h3 class="status-good">{dashboard_data['summary']['compliant_systems']}</h3>
                        <p>Compliant Systems</p>
                    </div>
                </div>
                
                <div class="card">
                    <div class="metric">
                        <h3 class="{'status-good' if dashboard_data['summary']['compliance_rate'] >= 80 else 'status-warning' if dashboard_data['summary']['compliance_rate'] >= 60 else 'status-critical'}">{dashboard_data['summary']['compliance_rate']:.1f}%</h3>
                        <p>Compliance Rate</p>
                    </div>
                </div>
                
                <div class="card">
                    <div class="metric">
                        <h3>{len(dashboard_data['recent_assessments'])}</h3>
                        <p>Recent Assessments</p>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>📈 Governance Level Distribution</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Governance Level</th>
                            <th>Number of Systems</th>
                            <th>Percentage</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(f'<tr><td>{level}</td><td>{count}</td><td>{count/dashboard_data["summary"]["total_systems"]*100 if dashboard_data["summary"]["total_systems"] > 0 else 0:.1f}%</td></tr>' for level, count in dashboard_data["governance_levels"].items())}
                    </tbody>
                </table>
            </div>
            
            <div class="card">
                <h3>🔍 Recent Compliance Assessments</h3>
                <table>
                    <thead>
                        <tr>
                            <th>System ID</th>
                            <th>Compliance Score</th>
                            <th>Status</th>
                            <th>Assessed At</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(f'<tr><td>{assessment["system_id"]}</td><td>{assessment["score"]:.1f}</td><td class="{"status-good" if assessment["status"] == "compliant" else "status-critical"}">{assessment["status"]}</td><td>{assessment["assessed_at"][:19]}</td></tr>' for assessment in dashboard_data["recent_assessments"][:10])}
                    </tbody>
                </table>
            </div>
            
            <div class="card">
                <h3>🔄 Actions</h3>
                <a href="/api/docs" class="btn" target="_blank">API Documentation</a>
                <a href="/systems" class="btn">Manage Systems</a>
                <a href="/workflows" class="btn">View Workflows</a>
                <button class="btn" onclick="location.reload()">Refresh Dashboard</button>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# API Routes

# System Management Endpoints
@app.post("/api/systems/register", response_model=Dict[str, Any], tags=["Systems"])
async def register_system(
    request: SystemRegistrationRequest,
    governance: GovernanceFramework = Depends(get_governance_framework)
):
    """Register a new AI system for governance."""
    try:
        system_info = request.dict()
        result = governance.register_ai_system(request.system_id, system_info)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/systems", response_model=Dict[str, Any], tags=["Systems"])
async def list_systems(governance: GovernanceFramework = Depends(get_governance_framework)):
    """List all registered AI systems."""
    return {
        "systems": list(governance.registered_systems.values()),
        "total_count": len(governance.registered_systems)
    }


@app.get("/api/systems/{system_id}", response_model=Dict[str, Any], tags=["Systems"])
async def get_system(
    system_id: str,
    governance: GovernanceFramework = Depends(get_governance_framework)
):
    """Get details of a specific AI system."""
    if system_id not in governance.registered_systems:
        raise HTTPException(status_code=404, detail="System not found")
    
    return governance.registered_systems[system_id]


# Compliance Assessment Endpoints
@app.post("/api/compliance/assess/{system_id}", response_model=ComplianceAssessmentResponse, tags=["Compliance"])
async def assess_system_compliance(
    system_id: str,
    governance: GovernanceFramework = Depends(get_governance_framework)
):
    """Run comprehensive compliance assessment for a system."""
    if system_id not in governance.registered_systems:
        raise HTTPException(status_code=404, detail="System not found")
    
    try:
        assessment = governance.assess_system_compliance(system_id)
        return ComplianceAssessmentResponse(
            system_id=system_id,
            overall_score=assessment["overall_score"],
            compliance_status=assessment["status"],
            module_assessments=assessment["module_assessments"],
            recommendations=governance.registered_systems[system_id].get("governance_requirements", []),
            assessed_at=assessment["last_assessed"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/compliance/dashboard", response_model=Dict[str, Any], tags=["Compliance"])
async def get_compliance_dashboard(governance: GovernanceFramework = Depends(get_governance_framework)):
    """Get governance dashboard data."""
    return governance.get_governance_dashboard()


# Workflow Management Endpoints
@app.post("/api/workflows/initiate", response_model=Dict[str, Any], tags=["Workflows"])
async def initiate_workflow(
    request: WorkflowInitiationRequest,
    orchestrator: WorkflowOrchestrator = Depends(get_workflow_orchestrator)
):
    """Initiate a new governance workflow."""
    try:
        context = {
            "system_id": request.system_id,
            **request.additional_context
        }
        result = orchestrator.initiate_workflow(request.template_id, context)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/workflows", response_model=Dict[str, Any], tags=["Workflows"])
async def list_workflows(
    status: Optional[str] = Query(None, description="Filter by workflow status"),
    workflow_type: Optional[str] = Query(None, description="Filter by workflow type"),
    orchestrator: WorkflowOrchestrator = Depends(get_workflow_orchestrator)
):
    """List workflows with optional filtering."""
    return orchestrator.list_workflows(status, workflow_type)


@app.get("/api/workflows/{workflow_id}/status", response_model=Dict[str, Any], tags=["Workflows"])
async def get_workflow_status(
    workflow_id: str,
    orchestrator: WorkflowOrchestrator = Depends(get_workflow_orchestrator)
):
    """Get status of a specific workflow."""
    try:
        return orchestrator.get_workflow_status(workflow_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/workflows/{workflow_id}/execute", response_model=Dict[str, Any], tags=["Workflows"])
async def execute_workflow_step(
    workflow_id: str,
    step_data: Optional[Dict[str, Any]] = None,
    orchestrator: WorkflowOrchestrator = Depends(get_workflow_orchestrator)
):
    """Execute the next step in a workflow."""
    try:
        return orchestrator.execute_workflow_step(workflow_id, step_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Model Risk Management Endpoints
@app.post("/api/model-risk/validate/{system_id}", response_model=Dict[str, Any], tags=["Model Risk"])
async def validate_model(
    system_id: str,
    validation_data: Dict[str, Any],
    governance: GovernanceFramework = Depends(get_governance_framework)
):
    """Perform model validation."""
    if system_id not in governance.registered_systems:
        raise HTTPException(status_code=404, detail="System not found")
    
    try:
        result = governance.model_risk_manager.validate_model(system_id, validation_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/model-risk/report/{system_id}", response_model=Dict[str, Any], tags=["Model Risk"])
async def get_model_risk_report(
    system_id: str,
    governance: GovernanceFramework = Depends(get_governance_framework)
):
    """Get comprehensive model risk report."""
    if system_id not in governance.registered_systems:
        raise HTTPException(status_code=404, detail="System not found")
    
    try:
        return governance.model_risk_manager.get_model_report(system_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Health check endpoint
@app.get("/health", response_model=Dict[str, str], tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)