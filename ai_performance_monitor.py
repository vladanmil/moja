#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - AI Performance Monitor
Prati kvalitet AI odgovora i korisničku satisfakciju
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import logging

logger = logging.getLogger(__name__)

@dataclass
class ResponseQuality:
    """Kvalitet AI odgovora"""
    question: str
    response: str
    response_time: float
    user_satisfaction: float
    ai_module_used: str
    confidence_score: float
    timestamp: datetime
    context: Dict[str, Any]

@dataclass
class UserSatisfaction:
    """Korisnička satisfakcija"""
    user_id: str
    question_type: str
    satisfaction_score: float
    feedback_text: str
    timestamp: datetime
    ai_module: str

@dataclass
class LearningProgress:
    """Napredak u učenju"""
    module_name: str
    success_rate: float
    total_interactions: int
    improvement_trend: float
    last_updated: datetime

class AIPerformanceMonitor:
    """Napredni monitor za AI performanse"""
    
    def __init__(self, performance_file: str = "ai_performance.json"):
        self.performance_file = performance_file
        
        # Glavni podaci
        self.response_qualities: List[ResponseQuality] = []
        self.user_satisfactions: List[UserSatisfaction] = []
        self.learning_progress: Dict[str, LearningProgress] = {}
        
        # Statistike
        self.total_responses = 0
        self.average_satisfaction = 0.0
        self.average_response_time = 0.0
        
        # Cache za brz pristup
        self.recent_performance: deque = deque(maxlen=100)
        self.module_performance: Dict[str, Dict[str, float]] = defaultdict(lambda: {
            'total_responses': 0,
            'average_satisfaction': 0.0,
            'success_rate': 0.0
        })
        
        # Učitaj postojeće podatke
        self._load_performance_data()
        
        logger.info("📊 AI Performance Monitor uspešno inicijalizovan!")
    
    def _load_performance_data(self):
        """Učitava postojeće podatke o performansama"""
        try:
            with open(self.performance_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Učitaj response qualities
                for resp_data in data.get('response_qualities', []):
                    resp_data['timestamp'] = datetime.fromisoformat(resp_data['timestamp'])
                    self.response_qualities.append(ResponseQuality(**resp_data))
                
                # Učitaj user satisfactions
                for sat_data in data.get('user_satisfactions', []):
                    sat_data['timestamp'] = datetime.fromisoformat(sat_data['timestamp'])
                    self.user_satisfactions.append(UserSatisfaction(**sat_data))
                
                # Učitaj learning progress
                for module_name, prog_data in data.get('learning_progress', {}).items():
                    prog_data['last_updated'] = datetime.fromisoformat(prog_data['last_updated'])
                    self.learning_progress[module_name] = LearningProgress(**prog_data)
                
                logger.info(f"✅ Učitano {len(self.response_qualities)} response qualities i {len(self.user_satisfactions)} user satisfactions")
                
        except FileNotFoundError:
            logger.info("📝 Kreiran novi performance fajl")
        except Exception as e:
            logger.error(f"❌ Greška pri učitavanju performance podataka: {e}")
    
    def _save_performance_data(self):
        """Čuva podatke o performansama"""
        try:
            data = {
                'response_qualities': [asdict(resp) for resp in self.response_qualities],
                'user_satisfactions': [asdict(sat) for sat in self.user_satisfactions],
                'learning_progress': {name: asdict(prog) for name, prog in self.learning_progress.items()}
            }
            
            # Konvertuj datetime u string za JSON
            for resp in data['response_qualities']:
                resp['timestamp'] = resp['timestamp'].isoformat()
            for sat in data['user_satisfactions']:
                sat['timestamp'] = sat['timestamp'].isoformat()
            for prog in data['learning_progress'].values():
                prog['last_updated'] = prog['last_updated'].isoformat()
            
            with open(self.performance_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.debug("💾 Performance podaci sačuvani")
            
        except Exception as e:
            logger.error(f"❌ Greška pri čuvanju performance podataka: {e}")
    
    def track_response_quality(self, question: str, response: str, ai_module: str, 
                              confidence_score: float = 0.5, context: Dict[str, Any] = None):
        """Prati kvalitet AI odgovora"""
        try:
            start_time = time.time()
            
            # Kreiraj response quality
            response_quality = ResponseQuality(
                question=question,
                response=response,
                response_time=time.time() - start_time,
                user_satisfaction=0.5,  # Default vrednost
                ai_module_used=ai_module,
                confidence_score=confidence_score,
                timestamp=datetime.now(),
                context=context or {}
            )
            
            self.response_qualities.append(response_quality)
            self.recent_performance.append(response_quality)
            
            # Ažuriraj statistike
            self.total_responses += 1
            self._update_module_performance(ai_module, response_quality)
            
            # Proveri da li treba da sačuvaš
            if self.total_responses % 10 == 0:
                self._save_performance_data()
            
            logger.info(f"📊 Response quality praćen: {ai_module} - {confidence_score:.2f}")
            
        except Exception as e:
            logger.error(f"❌ Greška pri praćenju response quality: {e}")
    
    def track_user_satisfaction(self, question: str, satisfaction_score: float, 
                               feedback_text: str = "", ai_module: str = "unknown", 
                               user_id: str = "default"):
        """Prati korisničku satisfakciju"""
        try:
            # Kreiraj user satisfaction
            user_satisfaction = UserSatisfaction(
                user_id=user_id,
                question_type=self._categorize_question(question),
                satisfaction_score=satisfaction_score,
                feedback_text=feedback_text,
                timestamp=datetime.now(),
                ai_module=ai_module
            )
            
            self.user_satisfactions.append(user_satisfaction)
            
            # Ažuriraj response quality ako postoji
            self._update_response_satisfaction(question, satisfaction_score)
            
            # Ažuriraj module performance
            self._update_module_satisfaction(ai_module, satisfaction_score)
            
            # Ažuriraj learning progress
            self._update_learning_progress(ai_module, satisfaction_score)
            
            logger.info(f"📊 User satisfaction praćen: {ai_module} - {satisfaction_score:.2f}")
            
        except Exception as e:
            logger.error(f"❌ Greška pri praćenju user satisfaction: {e}")
    
    def _categorize_question(self, question: str) -> str:
        """Kategorizuje pitanje"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['kako', 'kako da', 'how']):
            return "how_to"
        elif any(word in question_lower for word in ['šta', 'što', 'what']):
            return "what_is"
        elif any(word in question_lower for word in ['zašto', 'why']):
            return "why"
        elif any(word in question_lower for word in ['kada', 'when']):
            return "when"
        elif any(word in question_lower for word in ['gde', 'where']):
            return "where"
        else:
            return "general"
    
    def _update_response_satisfaction(self, question: str, satisfaction_score: float):
        """Ažurira satisfaction za response"""
        for resp in reversed(self.response_qualities):
            if resp.question.lower() in question.lower() or question.lower() in resp.question.lower():
                resp.user_satisfaction = satisfaction_score
                break
    
    def _update_module_performance(self, module_name: str, response_quality: ResponseQuality):
        """Ažurira performanse modula"""
        module_stats = self.module_performance[module_name]
        module_stats['total_responses'] += 1
        
        # Ažuriraj prosečno vreme odgovora
        total_time = module_stats.get('total_response_time', 0) + response_quality.response_time
        module_stats['total_response_time'] = total_time
        module_stats['average_response_time'] = total_time / module_stats['total_responses']
    
    def _update_module_satisfaction(self, module_name: str, satisfaction_score: float):
        """Ažurira satisfaction za modul"""
        module_stats = self.module_performance[module_name]
        
        # Ažuriraj prosečnu satisfakciju
        current_avg = module_stats['average_satisfaction']
        total_responses = module_stats['total_responses']
        
        new_avg = ((current_avg * (total_responses - 1)) + satisfaction_score) / total_responses
        module_stats['average_satisfaction'] = new_avg
    
    def _update_learning_progress(self, module_name: str, satisfaction_score: float):
        """Ažurira napredak u učenju"""
        if module_name not in self.learning_progress:
            self.learning_progress[module_name] = LearningProgress(
                module_name=module_name,
                success_rate=satisfaction_score,
                total_interactions=1,
                improvement_trend=0.0,
                last_updated=datetime.now()
            )
        else:
            progress = self.learning_progress[module_name]
            old_success_rate = progress.success_rate
            
            # Ažuriraj success rate
            total_interactions = progress.total_interactions + 1
            new_success_rate = ((old_success_rate * progress.total_interactions) + satisfaction_score) / total_interactions
            
            progress.success_rate = new_success_rate
            progress.total_interactions = total_interactions
            progress.improvement_trend = new_success_rate - old_success_rate
            progress.last_updated = datetime.now()
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Vraća statistiku performansi"""
        try:
            # Izračunaj generalne statistike
            if self.response_qualities:
                self.average_response_time = sum(r.response_time for r in self.response_qualities) / len(self.response_qualities)
            
            if self.user_satisfactions:
                self.average_satisfaction = sum(s.satisfaction_score for s in self.user_satisfactions) / len(self.user_satisfactions)
            
            # Top moduli po satisfakciji
            top_modules = sorted(
                self.module_performance.items(),
                key=lambda x: x[1]['average_satisfaction'],
                reverse=True
            )[:5]
            
            # Top moduli po broju odgovora
            most_used_modules = sorted(
                self.module_performance.items(),
                key=lambda x: x[1]['total_responses'],
                reverse=True
            )[:5]
            
            # Learning progress summary
            learning_summary = {}
            for module_name, progress in self.learning_progress.items():
                learning_summary[module_name] = {
                    'success_rate': progress.success_rate,
                    'total_interactions': progress.total_interactions,
                    'improvement_trend': progress.improvement_trend,
                    'last_updated': progress.last_updated.isoformat()
                }
            
            stats = {
                'total_responses': self.total_responses,
                'total_user_feedback': len(self.user_satisfactions),
                'average_satisfaction': round(self.average_satisfaction, 3),
                'average_response_time': round(self.average_response_time, 3),
                'top_modules_by_satisfaction': [
                    {'module': name, 'satisfaction': round(stats['average_satisfaction'], 3)}
                    for name, stats in top_modules
                ],
                'most_used_modules': [
                    {'module': name, 'responses': stats['total_responses']}
                    for name, stats in most_used_modules
                ],
                'learning_progress': learning_summary,
                'recent_performance': len(self.recent_performance),
                'performance_file_size': f"{len(self.response_qualities) * 0.001:.2f} KB"
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Greška pri dohvatanju performance statistike: {e}")
            return {"error": str(e)}
    
    def get_module_performance(self, module_name: str) -> Dict[str, Any]:
        """Vraća performanse određenog modula"""
        try:
            if module_name not in self.module_performance:
                return {"error": f"Modul {module_name} nije pronađen"}
            
            module_stats = self.module_performance[module_name]
            
            # Dohvati learning progress
            learning_progress = None
            if module_name in self.learning_progress:
                progress = self.learning_progress[module_name]
                learning_progress = {
                    'success_rate': progress.success_rate,
                    'total_interactions': progress.total_interactions,
                    'improvement_trend': progress.improvement_trend,
                    'last_updated': progress.last_updated.isoformat()
                }
            
            return {
                'module_name': module_name,
                'total_responses': module_stats['total_responses'],
                'average_satisfaction': round(module_stats['average_satisfaction'], 3),
                'average_response_time': round(module_stats.get('average_response_time', 0), 3),
                'learning_progress': learning_progress
            }
            
        except Exception as e:
            logger.error(f"❌ Greška pri dohvatanju module performance: {e}")
            return {"error": str(e)}
    
    def get_recent_performance(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Vraća nedavne performanse"""
        try:
            recent = []
            for resp in list(self.recent_performance)[-limit:]:
                recent.append({
                    'question': resp.question[:100] + "..." if len(resp.question) > 100 else resp.question,
                    'ai_module': resp.ai_module_used,
                    'confidence_score': round(resp.confidence_score, 3),
                    'response_time': round(resp.response_time, 3),
                    'user_satisfaction': round(resp.user_satisfaction, 3),
                    'timestamp': resp.timestamp.isoformat()
                })
            
            return recent
            
        except Exception as e:
            logger.error(f"❌ Greška pri dohvatanju recent performance: {e}")
            return []
    
    def clear_performance_data(self, module_name: str = None):
        """Briše performance podatke"""
        try:
            if module_name:
                # Briši samo određeni modul
                self.response_qualities = [r for r in self.response_qualities if r.ai_module_used != module_name]
                self.user_satisfactions = [s for s in self.user_satisfactions if s.ai_module != module_name]
                if module_name in self.learning_progress:
                    del self.learning_progress[module_name]
                if module_name in self.module_performance:
                    del self.module_performance[module_name]
                logger.info(f"🧹 Obrisani performance podaci za modul: {module_name}")
            else:
                # Briši sve podatke
                self.response_qualities.clear()
                self.user_satisfactions.clear()
                self.learning_progress.clear()
                self.module_performance.clear()
                self.recent_performance.clear()
                logger.info("🧹 Svi performance podaci obrisani")
            
            self._save_performance_data()
            
        except Exception as e:
            logger.error(f"❌ Greška pri brisanju performance podataka: {e}")

# Globalna instanca
ai_performance_monitor = None

def get_ai_performance_monitor() -> AIPerformanceMonitor:
    """Vraća globalnu instancu AI Performance Monitor-a"""
    global ai_performance_monitor
    if ai_performance_monitor is None:
        ai_performance_monitor = AIPerformanceMonitor()
    return ai_performance_monitor
