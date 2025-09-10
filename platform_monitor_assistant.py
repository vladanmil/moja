"""
Platform Monitor Assistant - Monitors platforms and provides insights
"""

import logging
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import json


class PlatformStatus(Enum):
    """Platform status indicators"""
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"
    ERROR = "error"


class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class PlatformMetrics:
    """Platform performance metrics"""
    platform_name: str
    response_time: float
    uptime_percentage: float
    error_rate: float
    active_users: int
    last_check: datetime
    status: PlatformStatus


@dataclass
class Alert:
    """Platform alert"""
    platform: str
    level: AlertLevel
    message: str
    timestamp: datetime
    resolved: bool = False


class PlatformMonitorAssistant:
    """Monitors platforms and provides insights"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.platforms = {}
        self.metrics_history = {}
        self.alerts = []
        self.monitoring_active = False
        self.logger = logging.getLogger(__name__)
        self._initialize_platforms()
    
    def _initialize_platforms(self):
        """Initialize platform monitoring"""
        default_platforms = [
            'textbroker', 'iwriter', 'amazon_mturk', 'clickworker', 'appen', 'lionbridge'
        ]
        
        for platform in default_platforms:
            self.platforms[platform] = {
                'enabled': True,
                'check_interval': 300,  # 5 minutes
                'last_check': None,
                'thresholds': {
                    'response_time': 5.0,
                    'error_rate': 0.05,
                    'uptime': 0.95
                }
            }
    
    def add_platform(self, platform_name: str, config: Dict) -> bool:
        """Add a new platform to monitor"""
        try:
            self.platforms[platform_name] = {
                'enabled': config.get('enabled', True),
                'check_interval': config.get('check_interval', 300),
                'last_check': None,
                'thresholds': config.get('thresholds', {
                    'response_time': 5.0,
                    'error_rate': 0.05,
                    'uptime': 0.95
                })
            }
            
            self.logger.info(f"Added platform: {platform_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding platform {platform_name}: {e}")
            return False
    
    def check_platform_health(self, platform_name: str) -> Optional[PlatformMetrics]:
        """Check health of a specific platform"""
        try:
            if platform_name not in self.platforms:
                self.logger.warning(f"Platform {platform_name} not found")
                return None
            
            # Simulate platform health check
            metrics = self._simulate_health_check(platform_name)
            
            # Store metrics
            if platform_name not in self.metrics_history:
                self.metrics_history[platform_name] = []
            
            self.metrics_history[platform_name].append(metrics)
            
            # Keep only recent metrics (last 100)
            if len(self.metrics_history[platform_name]) > 100:
                self.metrics_history[platform_name] = self.metrics_history[platform_name][-100:]
            
            # Check for alerts
            self._check_alerts(platform_name, metrics)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error checking platform health for {platform_name}: {e}")
            return None
    
    def _simulate_health_check(self, platform_name: str) -> PlatformMetrics:
        """Simulate platform health check"""
        import random
        
        # Simulate response time (0.1 to 10 seconds)
        response_time = random.uniform(0.1, 10.0)
        
        # Simulate uptime (90% to 99.9%)
        uptime = random.uniform(0.90, 0.999)
        
        # Simulate error rate (0% to 10%)
        error_rate = random.uniform(0.0, 0.10)
        
        # Simulate active users
        active_users = random.randint(100, 10000)
        
        # Determine status based on metrics
        if error_rate > 0.05 or response_time > 5.0:
            status = PlatformStatus.DEGRADED
        elif error_rate > 0.10:
            status = PlatformStatus.ERROR
        elif uptime < 0.95:
            status = PlatformStatus.MAINTENANCE
        else:
            status = PlatformStatus.ONLINE
        
        return PlatformMetrics(
            platform_name=platform_name,
            response_time=response_time,
            uptime_percentage=uptime,
            error_rate=error_rate,
            active_users=active_users,
            last_check=datetime.now(),
            status=status
        )
    
    def _check_alerts(self, platform_name: str, metrics: PlatformMetrics):
        """Check for alerts based on metrics"""
        thresholds = self.platforms[platform_name]['thresholds']
        
        # Check response time
        if metrics.response_time > thresholds['response_time']:
            self._create_alert(platform_name, AlertLevel.WARNING, 
                             f"High response time: {metrics.response_time:.2f}s")
        
        # Check error rate
        if metrics.error_rate > thresholds['error_rate']:
            self._create_alert(platform_name, AlertLevel.ERROR,
                             f"High error rate: {metrics.error_rate:.2%}")
        
        # Check uptime
        if metrics.uptime_percentage < thresholds['uptime']:
            self._create_alert(platform_name, AlertLevel.CRITICAL,
                             f"Low uptime: {metrics.uptime_percentage:.2%}")
        
        # Check status
        if metrics.status == PlatformStatus.ERROR:
            self._create_alert(platform_name, AlertLevel.CRITICAL,
                             f"Platform is experiencing errors")
        elif metrics.status == PlatformStatus.OFFLINE:
            self._create_alert(platform_name, AlertLevel.CRITICAL,
                             f"Platform is offline")
    
    def _create_alert(self, platform: str, level: AlertLevel, message: str):
        """Create a new alert"""
        alert = Alert(
            platform=platform,
            level=level,
            message=message,
            timestamp=datetime.now()
        )
        
        self.alerts.append(alert)
        self.logger.warning(f"Alert created: {platform} - {level.value}: {message}")
    
    def get_platform_metrics(self, platform_name: str, hours: int = 24) -> List[PlatformMetrics]:
        """Get platform metrics for specified time period"""
        try:
            if platform_name not in self.metrics_history:
                return []
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            metrics = [
                m for m in self.metrics_history[platform_name]
                if m.last_check > cutoff_time
            ]
            
            return metrics
        except Exception as e:
            self.logger.error(f"Error getting metrics for {platform_name}: {e}")
            return []
    
    def get_active_alerts(self, platform: Optional[str] = None) -> List[Alert]:
        """Get active (unresolved) alerts"""
        alerts = [a for a in self.alerts if not a.resolved]
        
        if platform:
            alerts = [a for a in alerts if a.platform == platform]
        
        return alerts
    
    def resolve_alert(self, alert_index: int) -> bool:
        """Mark an alert as resolved"""
        try:
            if 0 <= alert_index < len(self.alerts):
                self.alerts[alert_index].resolved = True
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error resolving alert: {e}")
            return False
    
    def get_platform_summary(self) -> Dict[str, Any]:
        """Get summary of all platforms"""
        summary = {
            'total_platforms': len(self.platforms),
            'online_platforms': 0,
            'degraded_platforms': 0,
            'offline_platforms': 0,
            'active_alerts': len(self.get_active_alerts()),
            'platforms': {}
        }
        
        for platform_name in self.platforms:
            if platform_name in self.metrics_history and self.metrics_history[platform_name]:
                latest_metrics = self.metrics_history[platform_name][-1]
                
                if latest_metrics.status == PlatformStatus.ONLINE:
                    summary['online_platforms'] += 1
                elif latest_metrics.status == PlatformStatus.DEGRADED:
                    summary['degraded_platforms'] += 1
                elif latest_metrics.status == PlatformStatus.OFFLINE:
                    summary['offline_platforms'] += 1
                
                summary['platforms'][platform_name] = {
                    'status': latest_metrics.status.value,
                    'response_time': latest_metrics.response_time,
                    'uptime': latest_metrics.uptime_percentage,
                    'error_rate': latest_metrics.error_rate,
                    'last_check': latest_metrics.last_check.isoformat()
                }
        
        return summary
    
    def start_monitoring(self) -> bool:
        """Start platform monitoring"""
        try:
            self.monitoring_active = True
            self.logger.info("Platform monitoring started")
            return True
        except Exception as e:
            self.logger.error(f"Error starting monitoring: {e}")
            return False
    
    def stop_monitoring(self) -> bool:
        """Stop platform monitoring"""
        try:
            self.monitoring_active = False
            self.logger.info("Platform monitoring stopped")
            return True
        except Exception as e:
            self.logger.error(f"Error stopping monitoring: {e}")
            return False
    
    def clear_old_metrics(self, days: int = 7) -> int:
        """Clear old metrics data"""
        try:
            cutoff_time = datetime.now() - timedelta(days=days)
            cleared_count = 0
            
            for platform in self.metrics_history:
                original_count = len(self.metrics_history[platform])
                self.metrics_history[platform] = [
                    m for m in self.metrics_history[platform]
                    if m.last_check > cutoff_time
                ]
                cleared_count += original_count - len(self.metrics_history[platform])
            
            self.logger.info(f"Cleared {cleared_count} old metrics entries")
            return cleared_count
        except Exception as e:
            self.logger.error(f"Error clearing old metrics: {e}")
            return 0
