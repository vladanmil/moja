# core/automation/__init__.py
"""
AutoEarnPro Automation Module
Sadrži sve komponente za automatizaciju bot naloga.
"""

# Import osnovnih komponenti
try:
    from .account_creator import AccountCreator
    from .bot_manager import BotManager
    from .bot_identity_generator import BotIdentityGenerator
    from .captcha_solver import CaptchaSolver
    from .email_handler import EmailHandler
    from .proxy_rotator import ProxyRotator
    from .ai_integration import AIContentHub
    from .bot_ai_communication import BotAICommunication, CommunicationType
    from .master_orchestrator import MasterOrchestrator
    from .account_manager import AccountManager
    from .auto_earn_orchestrator import AutoEarnOrchestrator
    from .enhanced_account_manager import EnhancedAccountManager
    from .proxy_manager import ProxyManager
    from .advanced_features import simulate_typing
    from .automation_engine import AutomationEngine
    from .task_scheduler import TaskScheduler
    from .workflow_manager import WorkflowManager
    from .blog_strategy_engine import BlogStrategyEngine
    from .email_automation import EmailAutomation
    from .humanization_layer import HumanizationLayer
    from .job_detection_engine import JobDetectionEngine
    from .job_detector import JobDetector
    from .payout_logic_manager import PayoutLogicManager
    from .freelancing_executor import FreelancingExecutor
    from .iwriter_executor import IWriterExecutor
    from .survey_executor import SurveyExecutor
    from .textbroker_executor import TextBrokerExecutor
    from .platform_publisher import PlatformPublisher
    from .profile_manager import ProfileManager
    from .self_improving_automation import SelfImprovingAutomation
    from .smart_mouse_controller import SmartMouseController
    from .smart_task_switcher import SmartTaskSwitcher
    from .smart_workflow_manager import SmartWorkflowManager
    from .submission_delivery_engine import SubmissionDeliveryEngine
    from .task_error_integration import TaskErrorIntegration
    from .task_executor import TaskExecutor
    from .web_content_reader import WebContentReader
except ImportError as e:
    print(f"Warning: Some automation modules not available: {e}")

__all__ = [
    'AccountCreator',
    'BotManager', 
    'BotIdentityGenerator',
    'CaptchaSolver',
    'EmailHandler',
    'ProxyRotator',
    'AIContentHub',
    'BotAICommunication',
    'CommunicationType',
    'MasterOrchestrator',
    'AccountManager',
    'AutoEarnOrchestrator',
    'EnhancedAccountManager',
    'ProxyManager',
    'simulate_typing',
    'AutomationEngine',
    'TaskScheduler',
    'WorkflowManager',
    'BlogStrategyEngine',
    'EmailAutomation',
    'HumanizationLayer',
    'JobDetectionEngine',
    'JobDetector',
    'PayoutLogicManager',
    'FreelancingExecutor',
    'IWriterExecutor',
    'SurveyExecutor',
    'TextBrokerExecutor',
    'PlatformPublisher',
    'ProfileManager',
    'SelfImprovingAutomation',
    'SmartMouseController',
    'SmartTaskSwitcher',
    'SmartWorkflowManager',
    'SubmissionDeliveryEngine',
    'TaskErrorIntegration',
    'TaskExecutor',
    'WebContentReader'
]
