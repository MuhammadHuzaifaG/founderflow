from app.models.workflow import FounderWorkflow, WorkflowStep, DecisionCheckpoint

class WorkflowEngine:
    def __init__(self):
        self.templates = {
            "market_scan": FounderWorkflow(
                workflow_name="Market scan",
                summary="Rapidly map the market and identify the strongest likely opportunity lane.",
                steps=[
                    WorkflowStep(
                        name="Signal capture",
                        goal="Collect market signals and buyer behavior patterns.",
                        input_needed=["market", "company_name", "founder_goal"],
                        output_expected="Initial map of likely opportunity pockets.",
                    ),
                    WorkflowStep(
                        name="Pain prioritization",
                        goal="Identify urgent problems worth solving first.",
                        input_needed=["founder_goal", "context"],
                        output_expected="Priority list of pain themes.",
                    ),
                    WorkflowStep(
                        name="Validation design",
                        goal="Turn signals into founder-led validation experiments.",
                        input_needed=["founder_goal"],
                        output_expected="Decision-ready validation plan.",
                    ),
                ],
                decision_checkpoints=[
                    DecisionCheckpoint(
                        stage="After signal capture",
                        question="Which segment feels acute enough to justify a founder sprint?",
                        rationale="Low urgency signals waste time.",
                        owner="Founder",
                    ),
                    DecisionCheckpoint(
                        stage="After pain prioritization",
                        question="Which problem is both urgent and likely to have buying motivation?",
                        rationale="Avoid broad TAM stories without real pain.",
                        owner="Founder",
                    ),
                ],
                validation_summary="Test a narrow slice of the market before expanding scope.",
            ),
            "lead_generation": FounderWorkflow(
                workflow_name="Lead generation",
                summary="Turn a broad market into prioritized leads and outreach angles.",
                steps=[
                    WorkflowStep(
                        name="ICP definition",
                        goal="Define the ideal customer profile.",
                        input_needed=["market", "company_name", "founder_goal"],
                        output_expected="Target audience hypothesis.",
                    ),
                    WorkflowStep(
                        name="Lead list construction",
                        goal="Select buyer groups and signals.",
                        input_needed=["context", "market"],
                        output_expected="Promising lead clusters.",
                    ),
                    WorkflowStep(
                        name="Outreach strategy",
                        goal="Define the best message and process.",
                        input_needed=["founder_goal"],
                        output_expected="Founder-ready outreach approach.",
                    ),
                ],
                decision_checkpoints=[
                    DecisionCheckpoint(
                        stage="ICP definition",
                        question="Which profile is most likely to have immediate pain and buying authority?",
                        rationale="Prioritize reachability over broad TAM.",
                        owner="Founder",
                    ),
                    DecisionCheckpoint(
                        stage="Outreach strategy",
                        question="Does the message solve a real problem or just pitch a feature?",
                        rationale="Good outreach starts with evidence, not product narrative.",
                        owner="Founder",
                    ),
                ],
                validation_summary="Validate with real customer conversations, not just pipeline volume.",
            ),
            "customer_discovery": FounderWorkflow(
                workflow_name="Customer discovery",
                summary="Run a small but high-signal discovery loop.",
                steps=[
                    WorkflowStep(
                        name="Interview segmentation",
                        goal="Choose the first customer segment to study.",
                        input_needed=["market", "founder_goal"],
                        output_expected="Interview target list.",
                    ),
                    WorkflowStep(
                        name="Question design",
                        goal="Probe pain, urgency, and alternatives.",
                        input_needed=["context", "founder_goal"],
                        output_expected="Interview questions and risk areas.",
                    ),
                    WorkflowStep(
                        name="Insight synthesis",
                        goal="Convert interview notes into a recommendation.",
                        input_needed=["context"],
                        output_expected="Recurring patterns and next experiments.",
                    ),
                ],
                decision_checkpoints=[
                    DecisionCheckpoint(
                        stage="Interview segmentation",
                        question="Which segment is likely to reveal the strongest signal before a product decision?",
                        rationale="Avoid broad discovery that creates noise.",
                        owner="Founder",
                    ),
                    DecisionCheckpoint(
                        stage="Insight synthesis",
                        question="Which insight materially changes roadmap or strategy?",
                        rationale="Not every opinion deserves equal weight.",
                        owner="Founder",
                    ),
                ],
                validation_summary="Only move forward when the core problem and buying trigger are clear.",
            ),
            "competitive_analysis": FounderWorkflow(
                workflow_name="Competitive analysis",
                summary="Identify meaningful market gaps and a realistic win strategy.",
                steps=[
                    WorkflowStep(
                        name="Competitor map",
                        goal="Identify direct and adjacent alternatives.",
                        input_needed=["market", "company_name"],
                        output_expected="Competitor landscape summary.",
                    ),
                    WorkflowStep(
                        name="Gap analysis",
                        goal="Find buyer pain not solved well enough.",
                        input_needed=["context", "founder_goal"],
                        output_expected="Opportunity and weak-spot map.",
                    ),
                    WorkflowStep(
                        name="Win strategy",
                        goal="Define how to compete realistically.",
                        input_needed=["founder_goal"],
                        output_expected="Positioning and winning angle.",
                    ),
                ],
                decision_checkpoints=[
                    DecisionCheckpoint(
                        stage="Gap analysis",
                        question="Is the gap real, important, and accessible enough to matter?",
                        rationale="The best openings are not always the most obvious.",
                        owner="Founder",
                    ),
                    DecisionCheckpoint(
                        stage="Win strategy",
                        question="Can the startup win via distribution, workflow fit, or depth?",
                        rationale="Category hype is less important than a realistic wedge.",
                        owner="Founder",
                    ),
                ],
                validation_summary="Competition evidence must be checked against actual customer access and product ability.",
            ),
            "meeting_summary": FounderWorkflow(
                workflow_name="Meeting summary",
                summary="Turn discussions into action, decisions, and follow-ups.",
                steps=[
                    WorkflowStep(
                        name="Decision extraction",
                        goal="Identify what actually changed the business direction.",
                        input_needed=["context"],
                        output_expected="Decision log.",
                    ),
                    WorkflowStep(
                        name="Action mapping",
                        goal="Turn commitments into tasks and owners.",
                        input_needed=["context", "founder_goal"],
                        output_expected="Action plan.",
                    ),
                    WorkflowStep(
                        name="Risk review",
                        goal="Highlight blockers and unresolved assumptions.",
                        input_needed=["context"],
                        output_expected="Risks and follow-ups.",
                    ),
                ],
                decision_checkpoints=[
                    DecisionCheckpoint(
                        stage="Decision extraction",
                        question="Which decisions changed the business versus which were just discussion?",
                        rationale="Not every meeting outcome matters equally.",
                        owner="Founder",
                    ),
                    DecisionCheckpoint(
                        stage="Risk review",
                        question="What is still ambiguous, and who owns the next step?",
                        rationale="The summary should reduce ambiguity, not increase it.",
                        owner="Founder",
                    ),
                ],
                validation_summary="A useful summary turns discussion into clear ownership and next steps.",
            ),
            "investor_prep": FounderWorkflow(
                workflow_name="Investor prep",
                summary="Structure the story around clear evidence and credible momentum.",
                steps=[
                    WorkflowStep(
                        name="Story frame",
                        goal="Define the problem, traction, and timing clearly.",
                        input_needed=["company_name", "market", "founder_goal"],
                        output_expected="Core investor story.",
                    ),
                    WorkflowStep(
                        name="Evidence check",
                        goal="Separate strong facts from weak claims.",
                        input_needed=["context", "founder_goal"],
                        output_expected="Evidence-backed narrative plan.",
                    ),
                    WorkflowStep(
                        name="Question readiness",
                        goal="Prepare likely objections and founder responses.",
                        input_needed=["context"],
                        output_expected="Objection map and response plan.",
                    ),
                ],
                decision_checkpoints=[
                    DecisionCheckpoint(
                        stage="Story frame",
                        question="Which version of the story is clearest and most defensible?",
                        rationale="Investor narratives work best when they are clear and credible.",
                        owner="Founder",
                    ),
                    DecisionCheckpoint(
                        stage="Question readiness",
                        question="What assumptions are most exposed if an investor pushes hard?",
                        rationale="Strong preparation surfaces weakness before it hits the room.",
                        owner="Founder",
                    ),
                ],
                validation_summary="The founder must decide what to say, omit, and validate before pitching.",
            ),
        }

    def get_workflow(self, task_type: str) -> FounderWorkflow:
        return self.templates.get(task_type, self.templates["market_scan"])