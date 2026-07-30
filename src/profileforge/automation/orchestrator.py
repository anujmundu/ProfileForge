"""Automation Orchestrator Implementation.

Master coordinator combining Workflow, RetryPolicy, Scheduler, and ExecutionReport.
Governed by 03_SYSTEM_ARCHITECTURE_SPEC.md and 06_ENGINE_LIFECYCLE_SPECIFICATION.md.
"""

import uuid
from datetime import UTC, datetime

from profileforge import __version__
from profileforge.automation.cancellation import CancellationToken
from profileforge.automation.diagnostics import AutomationDiagnostics
from profileforge.automation.models import (
    AutomationConfiguration,
    ExecutionReport,
    WorkflowResult,
)
from profileforge.automation.retry import AutomationRetryPolicy
from profileforge.automation.scheduler import ManualScheduler
from profileforge.automation.workflow import Workflow
from profileforge.github import GitHubClient


class AutomationOrchestrator:
    """Master orchestrator for automated workflow execution and reporting."""

    def __init__(
        self,
        config: AutomationConfiguration | None = None,
        github_client: GitHubClient | None = None,
    ) -> None:
        self.config = config or AutomationConfiguration()
        self.github_client = github_client
        self.workflow = Workflow(
            config=self.config, github_client=self.github_client
        )
        self.retry_policy = AutomationRetryPolicy(
            max_retries=self.config.max_retries,
            backoff_factor=self.config.retry_backoff_factor,
        )
        self.scheduler = ManualScheduler()

    @property
    def diagnostics(self) -> AutomationDiagnostics:
        """Get workflow execution diagnostics tracker."""
        return self.workflow.diagnostics

    def execute_workflow(
        self, username: str, cancel_token: CancellationToken | None = None
    ) -> ExecutionReport:
        """Execute end-to-end automation workflow with retry policy and reporting.

        Args:
            username: Target GitHub username.
            cancel_token: Optional cooperative cancellation token.

        Returns:
            ExecutionReport containing full WorkflowResult telemetry.
        """
        start_ts = datetime.now(UTC).isoformat()
        workflow_id = f"wf_{uuid.uuid4().hex[:8]}"

        def _run_action() -> WorkflowResult:
            return self.workflow.run(username=username, cancel_token=cancel_token)

        # Execute via scheduler + retry policy
        result: WorkflowResult = self.scheduler.schedule(
            lambda: self.retry_policy.execute(_run_action)
        )
        end_ts = datetime.now(UTC).isoformat()
        cfg_hash = f"dir={self.config.output_dir}_retries={self.config.max_retries}_pub={self.config.publisher_type}"

        return ExecutionReport(
            workflow_id=workflow_id,
            username=username,
            version=__version__,
            config_hash=cfg_hash,
            execution_mode="manual",
            start_timestamp=start_ts,
            end_timestamp=end_ts,
            result=result,
            metadata={
                "publisher": self.config.publisher_type,
                "output_dir": self.config.output_dir,
                "diagnostics": self.diagnostics.get_summary(),
            },
        )
