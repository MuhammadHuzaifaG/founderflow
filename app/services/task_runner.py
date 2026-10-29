from typing import Any, Dict, List

from app.models.founder_task import FounderTaskInput
from app.services.gemini_service import GeminiService
from app.services.lead_builder import LeadBuilder
from app.services.workflow_engine import WorkflowEngine
from app.utils.validators import sanitize_text

class TaskRunner:
    def __init__(self):
        self.gemini = GeminiService()
        self.workflow_engine = WorkflowEngine()
        self.lead_builder = LeadBuilder()

    async def run_task(self, task: FounderTaskInput) -> Dict[str, Any]:
        if not self.gemini.is_ready():
            raise RuntimeError("Gemini is not configured. Set GOOGLE_API_KEY in Vercel.")

        workflow = self.workflow_engine.get_workflow(task.task_type)
        prompt = self._build_prompt(task, workflow)
        system_prompt = self._build_system_prompt(task.task_type, workflow)
        result_text = await self.gemini.generate(prompt, system_prompt)
        parsed = self._parse_response(result_text)

        if task.task_type == "lead_generation":
            lead_result = self.lead_builder.build(
                task.company_name,
                task.market,
                task.founder_goal,
                task.context or "",
            )
            parsed["lead_generation"] = lead_result.model_dump()

        return {
            "task_type": task.task_type,
            "company_name": task.company_name,
            "summary": parsed["summary"],
            "findings": parsed["findings"],
            "recommended_next_steps": parsed["recommended_next_steps"],
            "confidence": parsed["confidence"],
            "human_judgment_required": True,
            "workflow": {
                "workflow_name": workflow.workflow_name,
                "steps": [step.model_dump() for step in workflow.steps],
                "decision_checkpoints": [cp.model_dump() for cp in workflow.decision_checkpoints],
                "validation_summary": workflow.validation_summary,
            },
            "lead_generation": parsed.get("lead_generation"),
        }

    def _build_prompt(self, task: FounderTaskInput, workflow) -> str:
        safe_company = sanitize_text(task.company_name, 120)
        safe_market = sanitize_text(task.market, 200)
        safe_goal = sanitize_text(task.founder_goal, 4000)
        safe_context = sanitize_text(task.context or "No extra context provided.", 8000)

        steps = "\n".join(f"- {item.name}: {item.goal}" for item in workflow.steps)
        checkpoints = "\n".join(f"- {item.stage}: {item.question}" for item in workflow.decision_checkpoints)

        return f"""
        Founder task: {task.task_type}
        Workflow: {workflow.workflow_name}

        Company: {safe_company}
        Market: {safe_market}
        Founder goal: {safe_goal}

        Context:
        {safe_context}

        Workflow steps:
        {steps}

        Required critical questions:
        {checkpoints}

        Deliver output in exact structure:
        Summary: ...
        Findings:
        - ...
        - ...
        - ...
        Recommended next steps:
        - ...
        - ...
        - ...
        Confidence: 0.00 to 1.00

        Rules:
        - Focus on reducing founder workload, not replacing judgment
        - Be direct and action-oriented
        - Keep output practical and realistic
        - Clearly state uncertainty
        - Highlight what a founder must validate manually
        """

    def _build_system_prompt(self, task_type: str, workflow) -> str:
        return (
            "You are a founder-focused AI strategist. "
            "Your job is to save the founder time without making the decision for them. "
            f"This workflow is: {workflow.workflow_name}. "
            f"Task type: {task_type}. "
            "Use sharp business judgment. "
            "Be honest about uncertainty. "
            "Prefer concrete and decision-oriented advice over generic startup advice. "
            "Always include a human validation note."
        )

    def _parse_response(self, response: str) -> Dict[str, Any]:
        lines = [line.strip() for line in response.splitlines() if line.strip()]
        summary = ""
        findings: List[str] = []
        next_steps: List[str] = []
        confidence = 0.75
        current_section = None

        for line in lines:
            lowered = line.lower()

            if lowered.startswith("summary:"):
                summary = line.split(":", 1)[1].strip()
                current_section = "summary"
                continue

            if lowered.startswith("findings:"):
                current_section = "findings"
                continue

            if lowered.startswith("recommended next steps:"):
                current_section = "next_steps"
                continue

            if lowered.startswith("confidence:"):
                try:
                    confidence = float(line.split(":", 1)[1].strip())
                except ValueError:
                    confidence = 0.75
                current_section = "confidence"
                continue

            if line.startswith("- "):
                item = line[2:].strip()
                if current_section == "findings" and item:
                    findings.append(item)
                elif current_section == "next_steps" and item:
                    next_steps.append(item)

        if not summary:
            summary = "The strongest opportunities are emerging, but they require manual validation before the founder commits more time or capital."

        if not findings:
            findings = [
                "The current opportunity is promising but not yet validated at a customer level.",
                "Founder judgment is needed to determine which insight is actually worth acting on.",
                "The market signal is relevant, but urgency and willingness to pay must be checked directly.",
            ]

        if not next_steps:
            next_steps = [
                "Run a short customer validation loop with 5-8 realistic users.",
                "Validate the top 2 assumptions before expanding the go-to-market push.",
                "Turn the strongest insight into a minimal experiment with a clear decision rule.",
            ]

        confidence = max(0.0, min(1.0, confidence))

        return {
            "summary": summary,
            "findings": findings[:5],
            "recommended_next_steps": next_steps[:5],
            "confidence": confidence,
        }