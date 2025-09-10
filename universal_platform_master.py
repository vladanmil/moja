#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - Universal Platform Master
Univerzalno upravljanje platformama za AutoEarnPro 2.0
"""

import logging
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import random

class PlatformStatus(Enum):
    """Platform status"""
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"
    MAINTENANCE = "maintenance"

@dataclass
class PlatformConfig:
    """Platform configuration"""
    name: str
    enabled: bool = True
    max_concurrent_tasks: int = 5
    task_timeout: int = 300
    retry_attempts: int = 3
    delay_between_actions: float = 2.0
    random_delays: bool = True

@dataclass
class TaskResult:
    """Task result"""
    success: bool
    platform: str
    task_type: str
    result_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_time: float = 0.0
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class UniversalPlatformMaster:
    """Universal platform management system"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Platform management
        self.platforms: Dict[str, PlatformConfig] = {}
        self.platform_status: Dict[str, PlatformStatus] = {}
        self.active_tasks: Dict[str, List[str]] = {}
        self.task_results: List[TaskResult] = []
        
        # Threading
        self.task_threads: Dict[str, threading.Thread] = {}
        self.running = False
        self._lock = threading.RLock()
        
        # Callbacks
        self.task_callbacks: List[Callable[[TaskResult], None]] = []
        self.status_callbacks: List[Callable[[str, PlatformStatus], None]] = []
        
        # Initialize default platforms
        self._initialize_default_platforms()
        
        self.logger.info("🚀 Universal Platform Master initialized")
    
    def _initialize_default_platforms(self):
        """Initialize default platforms"""
        default_platforms = [
            "textbroker",
            "iwriter", 
            "medium",
            "surveys",
            "amazon_mturk",
            "clickworker",
            "appen",
            "lionbridge"
        ]
        
        for platform in default_platforms:
            self.add_platform(platform, PlatformConfig(
                name=platform,
                enabled=True,
                max_concurrent_tasks=5,
                task_timeout=300,
                retry_attempts=3,
                delay_between_actions=2.0,
                random_delays=True
            ))
    
    def add_platform(self, platform_name: str, config: PlatformConfig) -> bool:
        """Add a new platform"""
        try:
            with self._lock:
                self.platforms[platform_name] = config
                self.platform_status[platform_name] = PlatformStatus.STOPPED
                self.active_tasks[platform_name] = []
                
            self.logger.info(f"Added platform: {platform_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding platform {platform_name}: {e}")
            return False
    
    def remove_platform(self, platform_name: str) -> bool:
        """Remove a platform"""
        try:
            with self._lock:
                if platform_name in self.platforms:
                    # Stop platform if running
                    self.stop_platform(platform_name)
                    
                    # Remove from all collections
                    del self.platforms[platform_name]
                    del self.platform_status[platform_name]
                    del self.active_tasks[platform_name]
                    
                    self.logger.info(f"Removed platform: {platform_name}")
                    return True
                    
            return False
            
        except Exception as e:
            self.logger.error(f"Error removing platform {platform_name}: {e}")
            return False
    
    def start_platform(self, platform_name: str) -> bool:
        """Start a platform"""
        try:
            with self._lock:
                if platform_name not in self.platforms:
                    self.logger.error(f"Platform {platform_name} not found")
                    return False
                
                if self.platform_status[platform_name] == PlatformStatus.ACTIVE:
                    self.logger.warning(f"Platform {platform_name} is already active")
                    return True
                
                # Update status
                self.platform_status[platform_name] = PlatformStatus.ACTIVE
                
                # Notify callbacks
                self._notify_status_callbacks(platform_name, PlatformStatus.ACTIVE)
                
                self.logger.info(f"Started platform: {platform_name}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error starting platform {platform_name}: {e}")
            return False
    
    def stop_platform(self, platform_name: str) -> bool:
        """Stop a platform"""
        try:
            with self._lock:
                if platform_name not in self.platforms:
                    return False
                
                # Update status
                self.platform_status[platform_name] = PlatformStatus.STOPPED
                
                # Clear active tasks
                self.active_tasks[platform_name] = []
                
                # Notify callbacks
                self._notify_status_callbacks(platform_name, PlatformStatus.STOPPED)
                
                self.logger.info(f"Stopped platform: {platform_name}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error stopping platform {platform_name}: {e}")
            return False
    
    def pause_platform(self, platform_name: str) -> bool:
        """Pause a platform"""
        try:
            with self._lock:
                if platform_name not in self.platforms:
                    return False
                
                self.platform_status[platform_name] = PlatformStatus.PAUSED
                self._notify_status_callbacks(platform_name, PlatformStatus.PAUSED)
                
                self.logger.info(f"Paused platform: {platform_name}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error pausing platform {platform_name}: {e}")
            return False
    
    def execute_task(self, platform_name: str, task_type: str, task_data: Dict[str, Any]) -> TaskResult:
        """Execute a task on a platform"""
        start_time = time.time()
        
        try:
            # Check if platform is available
            if platform_name not in self.platforms:
                return TaskResult(
                    success=False,
                    platform=platform_name,
                    task_type=task_type,
                    error_message=f"Platform {platform_name} not found"
                )
            
            if self.platform_status[platform_name] != PlatformStatus.ACTIVE:
                return TaskResult(
                    success=False,
                    platform=platform_name,
                    task_type=task_type,
                    error_message=f"Platform {platform_name} is not active"
                )
            
            # Check concurrent task limit
            platform_config = self.platforms[platform_name]
            if len(self.active_tasks[platform_name]) >= platform_config.max_concurrent_tasks:
                return TaskResult(
                    success=False,
                    platform=platform_name,
                    task_type=task_type,
                    error_message=f"Platform {platform_name} has reached maximum concurrent tasks"
                )
            
            # Add task to active list
            task_id = f"{platform_name}_{task_type}_{int(time.time())}"
            self.active_tasks[platform_name].append(task_id)
            
            # Simulate task execution
            result = self._execute_platform_task(platform_name, task_type, task_data)
            
            # Remove from active tasks
            if task_id in self.active_tasks[platform_name]:
                self.active_tasks[platform_name].remove(task_id)
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Create task result
            task_result = TaskResult(
                success=result.get('success', False),
                platform=platform_name,
                task_type=task_type,
                result_data=result.get('data'),
                error_message=result.get('error'),
                execution_time=execution_time
            )
            
            # Add to results
            with self._lock:
                self.task_results.append(task_result)
            
            # Notify callbacks
            self._notify_task_callbacks(task_result)
            
            return task_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TaskResult(
                success=False,
                platform=platform_name,
                task_type=task_type,
                error_message=str(e),
                execution_time=execution_time
            )
    
    def _execute_platform_task(self, platform_name: str, task_type: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific platform task (simulated)"""
        # Simulate task execution
        time.sleep(random.uniform(1, 3))
        
        # Simulate success/failure
        success = random.random() > 0.1  # 90% success rate
        
        if success:
            return {
                'success': True,
                'data': {
                    'task_id': f"{platform_name}_{task_type}_{int(time.time())}",
                    'result': f"Task {task_type} completed successfully on {platform_name}",
                    'earnings': random.uniform(5, 50)
                }
            }
        else:
            return {
                'success': False,
                'error': f"Task {task_type} failed on {platform_name}"
            }
    
    def get_platform_status(self, platform_name: str) -> Optional[PlatformStatus]:
        """Get platform status"""
        return self.platform_status.get(platform_name)
    
    def get_all_platform_status(self) -> Dict[str, PlatformStatus]:
        """Get status of all platforms"""
        return self.platform_status.copy()
    
    def get_platform_stats(self, platform_name: str) -> Dict[str, Any]:
        """Get platform statistics"""
        try:
            platform_results = [r for r in self.task_results if r.platform == platform_name]
            
            total_tasks = len(platform_results)
            successful_tasks = len([r for r in platform_results if r.success])
            failed_tasks = total_tasks - successful_tasks
            
            success_rate = (successful_tasks / total_tasks * 100) if total_tasks > 0 else 0
            avg_execution_time = sum(r.execution_time for r in platform_results) / total_tasks if total_tasks > 0 else 0
            
            return {
                'platform': platform_name,
                'total_tasks': total_tasks,
                'successful_tasks': successful_tasks,
                'failed_tasks': failed_tasks,
                'success_rate': success_rate,
                'avg_execution_time': avg_execution_time,
                'active_tasks': len(self.active_tasks.get(platform_name, [])),
                'status': self.platform_status.get(platform_name, PlatformStatus.STOPPED).value
            }
            
        except Exception as e:
            self.logger.error(f"Error getting stats for {platform_name}: {e}")
            return {}
    
    def add_task_callback(self, callback: Callable[[TaskResult], None]):
        """Add task completion callback"""
        self.task_callbacks.append(callback)
    
    def add_status_callback(self, callback: Callable[[str, PlatformStatus], None]):
        """Add status change callback"""
        self.status_callbacks.append(callback)
    
    def _notify_task_callbacks(self, task_result: TaskResult):
        """Notify task callbacks"""
        for callback in self.task_callbacks:
            try:
                callback(task_result)
            except Exception as e:
                self.logger.error(f"Error in task callback: {e}")
    
    def _notify_status_callbacks(self, platform_name: str, status: PlatformStatus):
        """Notify status callbacks"""
        for callback in self.status_callbacks:
            try:
                callback(platform_name, status)
            except Exception as e:
                self.logger.error(f"Error in status callback: {e}")
    
    def shutdown(self):
        """Shutdown platform master"""
        try:
            self.running = False
            
            # Stop all platforms
            for platform_name in list(self.platforms.keys()):
                self.stop_platform(platform_name)
            
            self.logger.info("🔒 Universal Platform Master shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")

# Global platform master instance
_global_platform_master = None

def get_universal_platform_master(config: Optional[Dict[str, Any]] = None) -> UniversalPlatformMaster:
    """Get global platform master instance"""
    global _global_platform_master
    if _global_platform_master is None:
        _global_platform_master = UniversalPlatformMaster(config)
    return _global_platform_master
