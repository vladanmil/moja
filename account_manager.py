#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - Account Manager Module
Manages multiple platform accounts and credentials
"""

import logging
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import random
import hashlib
import base64
from cryptography.fernet import Fernet


class AccountStatus(Enum):
    """Account status indicators"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    BANNED = "banned"
    PENDING = "pending"
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    LIMITED = "limited"


class PlatformType(Enum):
    """Platform types"""
    FREELANCING = "freelancing"
    CONTENT_CREATION = "content_creation"
    SURVEYS = "surveys"
    MICRO_TASKS = "micro_tasks"
    CRYPTO = "crypto"
    SOCIAL_MEDIA = "social_media"
    E_COMMERCE = "e_commerce"


@dataclass
class AccountCredentials:
    """Account credentials (encrypted)"""
    username: str
    password_hash: str
    email: str
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    two_factor_secret: Optional[str] = None


@dataclass
class AccountInfo:
    """Account information"""
    account_id: str
    platform: str
    platform_type: PlatformType
    credentials: AccountCredentials
    status: AccountStatus
    created_at: datetime
    last_login: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    earnings_total: float = 0.0
    tasks_completed: int = 0
    rating: float = 0.0
    metadata: Dict[str, Any] = None


@dataclass
class AccountActivity:
    """Account activity log"""
    account_id: str
    activity_type: str
    description: str
    timestamp: datetime
    success: bool
    details: Dict[str, Any] = None


class AccountManager:
    """Manages multiple platform accounts and credentials"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.accounts = {}
        self.activity_log = []
        self.encryption_key = None
        self.platform_configs = {}
        self.logger = logging.getLogger(__name__)
        self._initialize_manager()

    def _initialize_manager(self):
        """Initialize account manager"""
        try:
            # Generate encryption key for credentials
            self.encryption_key = Fernet.generate_key()
            self.cipher = Fernet(self.encryption_key)

            # Initialize platform configurations
            self.platform_configs = {
                'upwork': {
                    'type': PlatformType.FREELANCING,
                    'requires_verification': True,
                    'max_accounts': 3,
                    'rate_limit': 100,  # requests per hour
                    'supported_features': ['job_search', 'proposal_submission', 'time_tracking']
                },
                'fiverr': {
                    'type': PlatformType.FREELANCING,
                    'requires_verification': True,
                    'max_accounts': 2,
                    'rate_limit': 50,
                    'supported_features': ['gig_creation', 'order_management', 'communication']
                },
                'freelancer': {
                    'type': PlatformType.FREELANCING,
                    'requires_verification': True,
                    'max_accounts': 2,
                    'rate_limit': 80,
                    'supported_features': ['project_bidding', 'milestone_management', 'dispute_resolution']
                },
                'textbroker': {
                    'type': PlatformType.CONTENT_CREATION,
                    'requires_verification': True,
                    'max_accounts': 1,
                    'rate_limit': 200,
                    'supported_features': ['article_writing', 'quality_rating', 'payment_tracking']
                },
                'iwriter': {
                    'type': PlatformType.CONTENT_CREATION,
                    'requires_verification': True,
                    'max_accounts': 1,
                    'rate_limit': 150,
                    'supported_features': ['content_creation', 'revision_management', 'earnings_tracking']
                },
                'surveymonkey': {
                    'type': PlatformType.SURVEYS,
                    'requires_verification': False,
                    'max_accounts': 5,
                    'rate_limit': 300,
                    'supported_features': ['survey_completion', 'reward_redemption', 'profile_management']
                },
                'swagbucks': {
                    'type': PlatformType.SURVEYS,
                    'requires_verification': False,
                    'max_accounts': 3,
                    'rate_limit': 250,
                    'supported_features': ['survey_completion', 'gift_card_redemption', 'referral_program']
                },
                'amazon_mturk': {
                    'type': PlatformType.MICRO_TASKS,
                    'requires_verification': True,
                    'max_accounts': 1,
                    'rate_limit': 500,
                    'supported_features': ['hit_completion', 'qualification_tests', 'payment_processing']
                },
                'binance': {
                    'type': PlatformType.CRYPTO,
                    'requires_verification': True,
                    'max_accounts': 2,
                    'rate_limit': 1000,
                    'supported_features': ['trading', 'staking', 'mining_pools']
                },
                'coinbase': {
                    'type': PlatformType.CRYPTO,
                    'requires_verification': True,
                    'max_accounts': 2,
                    'rate_limit': 800,
                    'supported_features': ['trading', 'staking', 'learn_earn']
                }
            }

            self.logger.info("Account manager initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing account manager: {e}")

    def add_account(self, platform: str, username: str, password: str, 
                   email: str, api_key: Optional[str] = None, 
                   api_secret: Optional[str] = None) -> Optional[str]:
        """Add a new account"""
        try:
            # Validate platform
            if platform not in self.platform_configs:
                self.logger.error(f"Unsupported platform: {platform}")
                return None

            # Check account limits
            if not self._can_add_account(platform):
                self.logger.error(f"Cannot add more accounts for platform: {platform}")
                return None

            # Generate account ID
            account_id = self._generate_account_id(platform, username)

            # Check if account already exists
            if account_id in self.accounts:
                self.logger.warning(f"Account already exists: {account_id}")
                return account_id

            # Hash password
            password_hash = self._hash_password(password)

            # Encrypt sensitive data
            encrypted_api_key = self._encrypt_data(api_key) if api_key else None
            encrypted_api_secret = self._encrypt_data(api_secret) if api_secret else None

            # Create credentials
            credentials = AccountCredentials(
                username=username,
                password_hash=password_hash,
                email=email,
                api_key=encrypted_api_key,
                api_secret=encrypted_api_secret
            )

            # Create account info
            account_info = AccountInfo(
                account_id=account_id,
                platform=platform,
                platform_type=self.platform_configs[platform]['type'],
                credentials=credentials,
                status=AccountStatus.PENDING,
                created_at=datetime.now(),
                metadata={}
            )

            # Store account
            self.accounts[account_id] = account_info

            # Log activity
            self._log_activity(account_id, "account_created", "Account created successfully", True)

            self.logger.info(f"Added account: {account_id} for platform: {platform}")
            return account_id

        except Exception as e:
            self.logger.error(f"Error adding account: {e}")
            return None

    def _can_add_account(self, platform: str) -> bool:
        """Check if can add more accounts for platform"""
        try:
            config = self.platform_configs.get(platform, {})
            max_accounts = config.get('max_accounts', 1)

            # Count existing accounts for platform
            existing_count = sum(
                1 for account in self.accounts.values()
                if account.platform == platform
            )

            return existing_count < max_accounts

        except Exception as e:
            self.logger.error(f"Error checking account limits: {e}")
            return False

    def _generate_account_id(self, platform: str, username: str) -> str:
        """Generate unique account ID"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            random_suffix = random.randint(1000, 9999)
            return f"{platform}_{username}_{timestamp}_{random_suffix}"
        except Exception as e:
            self.logger.error(f"Error generating account ID: {e}")
            return f"{platform}_{username}_{random.randint(100000, 999999)}"

    def _hash_password(self, password: str) -> str:
        """Hash password securely"""
        try:
            salt = hashlib.sha256(str(random.random()).encode()).hexdigest()[:16]
            hash_obj = hashlib.sha256((password + salt).encode())
            return salt + hash_obj.hexdigest()
        except Exception as e:
            self.logger.error(f"Error hashing password: {e}")
            return ""

    def _encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            if not data:
                return ""
            encrypted = self.cipher.encrypt(data.encode())
            return base64.b64encode(encrypted).decode()
        except Exception as e:
            self.logger.error(f"Error encrypting data: {e}")
            return ""

    def _decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            if not encrypted_data:
                return ""
            decoded = base64.b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            self.logger.error(f"Error decrypting data: {e}")
            return ""

    def verify_account(self, account_id: str) -> bool:
        """Verify account credentials"""
        try:
            if account_id not in self.accounts:
                self.logger.error(f"Account not found: {account_id}")
                return False

            account = self.accounts[account_id]

            # Simulate verification process
            verification_success = random.random() > 0.1  # 90% success rate

            if verification_success:
                account.status = AccountStatus.VERIFIED
                account.last_activity = datetime.now()
                self._log_activity(account_id, "account_verified", "Account verified successfully", True)
                self.logger.info(f"Account verified: {account_id}")
            else:
                account.status = AccountStatus.UNVERIFIED
                self._log_activity(account_id, "verification_failed", "Account verification failed", False)

            return verification_success

        except Exception as e:
            self.logger.error(f"Error verifying account: {e}")
            return False

    def login_account(self, account_id: str, password: str) -> bool:
        """Login to account"""
        try:
            if account_id not in self.accounts:
                self.logger.error(f"Account not found: {account_id}")
                return False

            account = self.accounts[account_id]

            # Verify password
            if not self._verify_password(password, account.credentials.password_hash):
                self._log_activity(account_id, "login_failed", "Invalid password", False)
                return False

            # Check account status
            if account.status not in [AccountStatus.ACTIVE, AccountStatus.VERIFIED]:
                self._log_activity(account_id, "login_failed", f"Account status: {account.status.value}", False)
                return False

            # Update login time
            account.last_login = datetime.now()
            account.last_activity = datetime.now()

            # Simulate login success
            login_success = random.random() > 0.05  # 95% success rate

            if login_success:
                self._log_activity(account_id, "login_success", "Login successful", True)
                self.logger.info(f"Login successful: {account_id}")
            else:
                self._log_activity(account_id, "login_failed", "Login failed", False)

            return login_success

        except Exception as e:
            self.logger.error(f"Error logging in: {e}")
            return False

    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password against stored hash"""
        try:
            if not stored_hash or len(stored_hash) < 16:
                return False

            salt = stored_hash[:16]
            hash_obj = hashlib.sha256((password + salt).encode())
            return salt + hash_obj.hexdigest() == stored_hash

        except Exception as e:
            self.logger.error(f"Error verifying password: {e}")
            return False

    def update_account_status(self, account_id: str, status: AccountStatus) -> bool:
        """Update account status"""
        try:
            if account_id not in self.accounts:
                self.logger.error(f"Account not found: {account_id}")
                return False

            account = self.accounts[account_id]
            old_status = account.status
            account.status = status
            account.last_activity = datetime.now()

            self._log_activity(
                account_id, 
                "status_updated", 
                f"Status changed from {old_status.value} to {status.value}", 
                True
            )

            self.logger.info(f"Updated account status: {account_id} -> {status.value}")
            return True

        except Exception as e:
            self.logger.error(f"Error updating account status: {e}")
            return False

    def get_account_info(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Get account information (without sensitive data)"""
        try:
            if account_id not in self.accounts:
                return None

            account = self.accounts[account_id]

            return {
                'account_id': account.account_id,
                'platform': account.platform,
                'platform_type': account.platform_type.value,
                'status': account.status.value,
                'created_at': account.created_at.isoformat(),
                'last_login': account.last_login.isoformat() if account.last_login else None,
                'last_activity': account.last_activity.isoformat() if account.last_activity else None,
                'earnings_total': account.earnings_total,
                'tasks_completed': account.tasks_completed,
                'rating': account.rating,
                'username': account.credentials.username,
                'email': account.credentials.email
            }

        except Exception as e:
            self.logger.error(f"Error getting account info: {e}")
            return None

    def get_accounts_by_platform(self, platform: str) -> List[Dict[str, Any]]:
        """Get all accounts for a specific platform"""
        try:
            accounts = []
            for account in self.accounts.values():
                if account.platform == platform:
                    account_info = self.get_account_info(account.account_id)
                    if account_info:
                        accounts.append(account_info)
            return accounts

        except Exception as e:
            self.logger.error(f"Error getting accounts by platform: {e}")
            return []

    def get_active_accounts(self) -> List[Dict[str, Any]]:
        """Get all active accounts"""
        try:
            active_accounts = []
            for account in self.accounts.values():
                if account.status in [AccountStatus.ACTIVE, AccountStatus.VERIFIED]:
                    account_info = self.get_account_info(account.account_id)
                    if account_info:
                        active_accounts.append(account_info)
            return active_accounts

        except Exception as e:
            self.logger.error(f"Error getting active accounts: {e}")
            return []

    def update_account_earnings(self, account_id: str, earnings: float) -> bool:
        """Update account earnings"""
        try:
            if account_id not in self.accounts:
                return False

            account = self.accounts[account_id]
            account.earnings_total += earnings
            account.last_activity = datetime.now()

            self._log_activity(
                account_id, 
                "earnings_updated", 
                f"Earnings updated: +${earnings:.2f}", 
                True,
                {'earnings': earnings}
            )

            return True

        except Exception as e:
            self.logger.error(f"Error updating account earnings: {e}")
            return False

    def update_account_tasks(self, account_id: str, tasks_completed: int = 1) -> bool:
        """Update account task count"""
        try:
            if account_id not in self.accounts:
                return False

            account = self.accounts[account_id]
            account.tasks_completed += tasks_completed
            account.last_activity = datetime.now()

            self._log_activity(
                account_id, 
                "tasks_updated", 
                f"Tasks completed: +{tasks_completed}", 
                True,
                {'tasks_completed': tasks_completed}
            )

            return True

        except Exception as e:
            self.logger.error(f"Error updating account tasks: {e}")
            return False

    def remove_account(self, account_id: str) -> bool:
        """Remove an account"""
        try:
            if account_id not in self.accounts:
                self.logger.error(f"Account not found: {account_id}")
                return False

            # Log removal
            self._log_activity(account_id, "account_removed", "Account removed", True)

            # Remove account
            del self.accounts[account_id]

            self.logger.info(f"Removed account: {account_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error removing account: {e}")
            return False

    def _log_activity(self, account_id: str, activity_type: str, description: str, 
                     success: bool, details: Optional[Dict] = None):
        """Log account activity"""
        try:
            activity = AccountActivity(
                account_id=account_id,
                activity_type=activity_type,
                description=description,
                timestamp=datetime.now(),
                success=success,
                details=details or {}
            )

            self.activity_log.append(activity)

            # Keep only recent activity (last 1000 entries)
            if len(self.activity_log) > 1000:
                self.activity_log = self.activity_log[-1000:]

        except Exception as e:
            self.logger.error(f"Error logging activity: {e}")

    def get_account_activity(self, account_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get account activity log"""
        try:
            activities = [
                activity for activity in self.activity_log
                if activity.account_id == account_id
            ]

            # Sort by timestamp (newest first)
            activities.sort(key=lambda x: x.timestamp, reverse=True)

            # Convert to dict format
            activity_list = []
            for activity in activities[:limit]:
                activity_list.append({
                    'activity_type': activity.activity_type,
                    'description': activity.description,
                    'timestamp': activity.timestamp.isoformat(),
                    'success': activity.success,
                    'details': activity.details
                })

            return activity_list

        except Exception as e:
            self.logger.error(f"Error getting account activity: {e}")
            return []

    def get_account_summary(self) -> Dict[str, Any]:
        """Get summary of all accounts"""
        try:
            total_accounts = len(self.accounts)
            active_accounts = len([a for a in self.accounts.values() 
                                 if a.status in [AccountStatus.ACTIVE, AccountStatus.VERIFIED]])
            
            total_earnings = sum(account.earnings_total for account in self.accounts.values())
            total_tasks = sum(account.tasks_completed for account in self.accounts.values())

            platform_breakdown = {}
            for account in self.accounts.values():
                platform = account.platform
                if platform not in platform_breakdown:
                    platform_breakdown[platform] = {
                        'count': 0,
                        'earnings': 0.0,
                        'tasks': 0
                    }
                platform_breakdown[platform]['count'] += 1
                platform_breakdown[platform]['earnings'] += account.earnings_total
                platform_breakdown[platform]['tasks'] += account.tasks_completed

            return {
                'total_accounts': total_accounts,
                'active_accounts': active_accounts,
                'total_earnings': total_earnings,
                'total_tasks': total_tasks,
                'platform_breakdown': platform_breakdown,
                'status_breakdown': {
                    status.value: len([a for a in self.accounts.values() if a.status == status])
                    for status in AccountStatus
                }
            }

        except Exception as e:
            self.logger.error(f"Error getting account summary: {e}")
            return {}

    def clear_old_activity(self, days: int = 30) -> int:
        """Clear old activity logs"""
        try:
            cutoff_time = datetime.now() - timedelta(days=days)
            original_count = len(self.activity_log)

            self.activity_log = [
                activity for activity in self.activity_log
                if activity.timestamp > cutoff_time
            ]

            cleared_count = original_count - len(self.activity_log)
            self.logger.info(f"Cleared {cleared_count} old activity entries")
            return cleared_count

        except Exception as e:
            self.logger.error(f"Error clearing old activity: {e}")
            return 0
