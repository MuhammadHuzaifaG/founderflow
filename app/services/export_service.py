from app.models.export import ExportSummary

class ExportService:
    def build_summary(self, task_data: dict) -> ExportSummary:
        return ExportSummary(
            company_name=task_data.get("company_name", "Unknown company"),
            task_type=task_data.get("task_type", "market_scan"),
            summary=task_data.get("summary", ""),
            findings=task_data.get("findings", []),
            next_steps=task_data.get("recommended_next_steps", []),
            confidence=float(task_data.get("confidence", 0.0)),
            created_at=task_data.get("created_at"),
        )

    def render_txt(self, summary: ExportSummary) -> str:
        lines = [
            "FounderFlow export",
            f"Company: {summary.company_name}",
            f"Task: {summary.task_type}",
            f"Created: {summary.created_at or 'n/a'}",
            "",
            "Summary:",
            summary.summary,
            "",
            "Key findings:",
        ]

        for idx, item in enumerate(summary.findings, start=1):
            lines.append(f"{idx}. {item}")

        lines.extend(["", "Recommended next steps:"])
        for idx, item in enumerate(summary.next_steps, start=1):
            lines.append(f"{idx}. {item}")

        lines.extend(["", f"Confidence: {summary.confidence:.2f}"])
        return "\n".join(lines)