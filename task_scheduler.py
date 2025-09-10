#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - Task Scheduler
Planer zadataka za automatizaciju
"""

import logging
import time
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class TaskScheduler:
    """Planer zadataka za automatizaciju"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.scheduled_tasks = []
        self.running = False
        
    def schedule_task(self, task: Dict[str, Any], schedule: Dict[str, Any]) -> bool:
        """Planira zadatak"""
        try:
            scheduled_task = {
                'task': task,
                'schedule': schedule,
                'next_run': self._calculate_next_run(schedule),
                'created_at': datetime.now()
            }
            self.scheduled_tasks.append(scheduled_task)
            self.logger.info(f"Planiran zadatak: {task.get('name', 'Unknown')}")
            return True
        except Exception as e:
            self.logger.error(f"Greška pri planiranju zadatka: {e}")
            return False
    
    def get_due_tasks(self) -> List[Dict[str, Any]]:
        """Vraća zadatke koji su na redu"""
        try:
            due_tasks = []
            current_time = datetime.now()
            
            for scheduled_task in self.scheduled_tasks:
                if scheduled_task['next_run'] <= current_time:
                    due_tasks.append(scheduled_task)
            
            return due_tasks
        except Exception as e:
            self.logger.error(f"Greška pri proveri zadataka: {e}")
            return []
    
    def update_task_schedule(self, task_id: str, new_schedule: Dict[str, Any]) -> bool:
        """Ažurira plan zadatka"""
        try:
            for scheduled_task in self.scheduled_tasks:
                if scheduled_task['task'].get('id') == task_id:
                    scheduled_task['schedule'] = new_schedule
                    scheduled_task['next_run'] = self._calculate_next_run(new_schedule)
                    self.logger.info(f"Ažuriran plan za zadatak: {task_id}")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Greška pri ažuriranju plana: {e}")
            return False
    
    def remove_task(self, task_id: str) -> bool:
        """Uklanja zadatak iz plana"""
        try:
            for i, scheduled_task in enumerate(self.scheduled_tasks):
                if scheduled_task['task'].get('id') == task_id:
                    del self.scheduled_tasks[i]
                    self.logger.info(f"Uklonjen zadatak iz plana: {task_id}")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Greška pri uklanjanju zadatka: {e}")
            return False
    
    def _calculate_next_run(self, schedule: Dict[str, Any]) -> datetime:
        """Računa sledeće izvršavanje"""
        current_time = datetime.now()
        
        if schedule.get('type') == 'interval':
            interval_minutes = schedule.get('interval_minutes', 60)
            return current_time + timedelta(minutes=interval_minutes)
        elif schedule.get('type') == 'daily':
            hour = schedule.get('hour', 9)
            minute = schedule.get('minute', 0)
            next_run = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_run <= current_time:
                next_run += timedelta(days=1)
            return next_run
        elif schedule.get('type') == 'weekly':
            day_of_week = schedule.get('day_of_week', 0)  # Monday = 0
            hour = schedule.get('hour', 9)
            minute = schedule.get('minute', 0)
            
            days_ahead = day_of_week - current_time.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            
            next_run = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
            next_run += timedelta(days=days_ahead)
            return next_run
        else:
            # Default: svaki sat
            return current_time + timedelta(hours=1)
