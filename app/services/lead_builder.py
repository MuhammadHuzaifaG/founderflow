from app.models.lead_score import LeadGenerationResult, LeadOpportunity
from app.utils.score_helpers import calculate_score

class LeadBuilder:
    def build(self, company_name: str, market: str, founder_goal: str, context: str = "") -> LeadGenerationResult:
        opportunities = [
            LeadOpportunity(
                name=f"{company_name} pilot lead",
                segment="Ops-focused SMB teams",
                urgency=9,
                fit=8,
                access=7,
                score=80,
                reason="Strong pain signal with a narrow and reachable decision-maker group.",
                next_step="Validate willingness to pay and decision-maker access with 3 outreach attempts.",
            ),
            LeadOpportunity(
                name="Decision-maker outreach lane",
                segment="Founders or COOs with scaling bottlenecks",
                urgency=8,
                fit=9,
                access=6,
                score=79,
                reason="Strong alignment with founder-led workflow needs and likely budget authority.",
                next_step="Test a short email sequence with a problem-first message.",
            ),
            LeadOpportunity(
                name="Product-led trial segment",
                segment="Teams already managing manual workflow pain",
                urgency=7,
                fit=9,
                access=8,
                score=78,
                reason="More reachable and easier to test in a lightweight pilot.",
                next_step="Create a minimum-value prototype or one-page test to gauge interest.",
            ),
        ]

        for item in opportunities:
            item.score = calculate_score(item.urgency, item.fit, item.access)

        return LeadGenerationResult(
            summary=(
                "The strongest opportunity is a narrow, reachable customer segment with a clear pain signal "
                "and a short path to validation."
            ),
            opportunity_cards=opportunities,
            founder_decision_prompt=(
                "Which opportunity is most likely to validate quickly with the least founder effort, and "
                "which should be deprioritized until stronger evidence exists?"
            ),
        )