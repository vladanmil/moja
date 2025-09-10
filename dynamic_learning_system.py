#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - Dynamic Learning System
Daje AI asistentu sposobnost da se prilagođava i uči u realnom vremenu
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import logging
import threading
import queue

logger = logging.getLogger(__name__)

@dataclass
class LearningRule:
    """Pravilo učenja"""
    id: str
    condition: str
    action: str
    priority: float
    success_rate: float
    usage_count: int
    last_used: datetime
    created: datetime
    context: Dict[str, Any]

@dataclass
class AdaptiveResponse:
    """Adaptivni odgovor"""
    pattern: str
    response: str
    confidence: float
    learning_score: float
    context_requirements: Dict[str, Any]

@dataclass
class UserBehavior:
    """Ponašanje korisnika"""
    user_id: str
    behavior_type: str
    frequency: int
    last_occurrence: datetime
    context: Dict[str, Any]
    satisfaction_history: List[float]

class DynamicLearningSystem:
    """Napredni sistem za dinamičko učenje AI asistenta"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Learning rules
        self.learning_rules: Dict[str, LearningRule] = {}
        self.adaptive_responses: Dict[str, AdaptiveResponse] = {}
        self.user_behaviors: Dict[str, UserBehavior] = {}
        
        # Learning patterns
        self.pattern_database: Dict[str, List[str]] = defaultdict(list)
        self.response_templates: Dict[str, List[str]] = defaultdict(list)
        
        # Real-time learning
        self.learning_queue = queue.Queue()
        self.is_learning = False
        self.learning_thread = None
        
        # Performance metrics
        self.learning_metrics = {
            'total_learnings': 0,
            'successful_adaptations': 0,
            'failed_adaptations': 0,
            'average_confidence': 0.0,
            'learning_speed': 0.0
        }
        
        # Initialize learning system
        self._initialize_learning_system()
        self._start_learning_thread()
        
        self.logger.info("🚀 Dynamic Learning System uspešno inicijalizovan!")
    
    def _initialize_learning_system(self):
        """Inicijalizuje learning sistem sa osnovnim pravilima"""
        try:
            # Osnovna pravila za učenje
            basic_rules = [
                {
                    'condition': 'user_asks_about_earning',
                    'action': 'provide_detailed_earning_strategy',
                    'priority': 0.9,
                    'context': {'topic': 'earning', 'complexity': 'detailed'}
                },
                {
                    'condition': 'user_asks_about_platforms',
                    'action': 'list_platforms_with_analysis',
                    'priority': 0.8,
                    'context': {'topic': 'platforms', 'complexity': 'comprehensive'}
                },
                {
                    'condition': 'user_expresses_frustration',
                    'action': 'provide_emotional_support_and_solutions',
                    'priority': 0.95,
                    'context': {'emotion': 'frustration', 'approach': 'supportive'}
                },
                {
                    'condition': 'user_asks_technical_question',
                    'action': 'provide_step_by_step_technical_guidance',
                    'priority': 0.85,
                    'context': {'topic': 'technical', 'complexity': 'step_by_step'}
                }
            ]
            
            for rule_data in basic_rules:
                rule = LearningRule(
                    id=f"rule_{len(self.learning_rules)}",
                    condition=rule_data['condition'],
                    action=rule_data['action'],
                    priority=rule_data['priority'],
                    success_rate=0.7,  # Početna vrednost
                    usage_count=0,
                    last_used=datetime.now(),
                    created=datetime.now(),
                    context=rule_data['context']
                )
                self.learning_rules[rule.id] = rule
            
            # Osnovni adaptivni odgovori
            basic_responses = [
                {
                    'pattern': 'kako da zaradim',
                    'response': '🎯 **AI Strategija za Zaradu:**\n\n1. **Diversifikacija platformi** - Koristite 10-15 platformi\n2. **Optimizacija vremena** - Fokus na najprofitabilne časove\n3. **AI automacija** - Koristite smart workflow\n4. **Kontinuirano učenje** - Pratite tržišne trendove\n\n💡 **AI Preporučujem:** Započnite sa "Auto Mode" + "AI Optimization"',
                    'confidence': 0.9,
                    'context_requirements': {'topic': 'earning', 'user_level': 'any'}
                },
                {
                    'pattern': 'koje su najbolje platforme',
                    'response': '🏆 **AI Analiza Platformi:**\n\n**Top 5 Platformi (AI-optimizovano):**\n1. **Textbroker** - $15-50/članak\n2. **Upwork** - $20-100/sat\n3. **Fiverr** - $5-500/projekat\n4. **Freelancer** - $15-80/sat\n5. **Guru** - $25-150/sat\n\n🚀 **AI Preporučujem:** Započnite sa Textbroker + Upwork kombinacijom',
                    'confidence': 0.85,
                    'context_requirements': {'topic': 'platforms', 'user_level': 'beginner'}
                }
            ]
            
            for resp_data in basic_responses:
                response = AdaptiveResponse(
                    pattern=resp_data['pattern'],
                    response=resp_data['response'],
                    confidence=resp_data['confidence'],
                    learning_score=0.8,
                    context_requirements=resp_data['context_requirements']
                )
                self.adaptive_responses[resp_data['pattern']] = response
            
            self.logger.info(f"✅ Inicijalizovano {len(self.learning_rules)} learning pravila i {len(self.adaptive_responses)} adaptivnih odgovora")
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri inicijalizaciji learning sistema: {e}")
    
    def _start_learning_thread(self):
        """Pokreće thread za real-time učenje"""
        try:
            self.is_learning = True
            self.learning_thread = threading.Thread(target=self._learning_worker, daemon=True)
            self.learning_thread.start()
            self.logger.info("🔄 Learning thread pokrenut")
        except Exception as e:
            self.logger.error(f"❌ Greška pri pokretanju learning thread-a: {e}")
    
    def _learning_worker(self):
        """Worker thread za procesiranje learning zahteva"""
        while self.is_learning:
            try:
                # Procesiraj learning zahteve
                try:
                    learning_request = self.learning_queue.get(timeout=1)
                    self._process_learning_request(learning_request)
                except queue.Empty:
                    continue
                
                # Periodično ažuriranje
                if time.time() % 60 < 1:  # Svaki minut
                    self._update_learning_metrics()
                    
            except Exception as e:
                self.logger.error(f"❌ Greška u learning worker-u: {e}")
                time.sleep(1)
    
    def _process_learning_request(self, request: Dict[str, Any]):
        """Procesira learning zahtev"""
        try:
            request_type = request.get('type')
            
            if request_type == 'user_feedback':
                self._learn_from_user_feedback(request)
            elif request_type == 'pattern_recognition':
                self._learn_pattern(request)
            elif request_type == 'response_adaptation':
                self._adapt_response(request)
            elif request_type == 'behavior_analysis':
                self._analyze_user_behavior(request)
            else:
                self.logger.warning(f"⚠️ Nepoznat tip learning zahteva: {request_type}")
                
        except Exception as e:
            self.logger.error(f"❌ Greška pri procesiranju learning zahteva: {e}")
    
    def _learn_from_user_feedback(self, feedback: Dict[str, Any]):
        """Uči iz feedback-a korisnika"""
        try:
            user_input = feedback.get('user_input', '')
            ai_response = feedback.get('ai_response', '')
            satisfaction = feedback.get('satisfaction', 0.5)
            context = feedback.get('context', {})
            
            # Analiziraj feedback i ažuriraj learning rules
            if satisfaction > 0.7:  # Pozitivan feedback
                self._reinforce_successful_pattern(user_input, ai_response, context)
            elif satisfaction < 0.3:  # Negativan feedback
                self._learn_from_failure(user_input, ai_response, context)
            
            # Ažuriraj user behavior
            self._update_user_behavior(feedback)
            
            self.logger.info(f"🧠 Naučeno iz feedback-a: satisfaction={satisfaction}")
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri učenju iz feedback-a: {e}")
    
    def _reinforce_successful_pattern(self, user_input: str, ai_response: str, context: Dict[str, Any]):
        """Pojačava uspešan obrazac"""
        try:
            # Pronađi postojeće pravilo ili kreiraj novo
            pattern_key = self._extract_pattern_key(user_input)
            
            if pattern_key in self.learning_rules:
                rule = self.learning_rules[pattern_key]
                rule.success_rate = min(1.0, rule.success_rate + 0.1)
                rule.usage_count += 1
                rule.last_used = datetime.now()
            else:
                # Kreiraj novo pravilo
                new_rule = LearningRule(
                    id=f"rule_{len(self.learning_rules)}",
                    condition=f"user_input_contains_{pattern_key}",
                    action="provide_similar_response",
                    priority=0.8,
                    success_rate=0.8,
                    usage_count=1,
                    last_used=datetime.now(),
                    created=datetime.now(),
                    context=context
                )
                self.learning_rules[new_rule.id] = new_rule
            
            # Ažuriraj adaptivni odgovor
            if pattern_key not in self.adaptive_responses:
                adaptive_response = AdaptiveResponse(
                    pattern=pattern_key,
                    response=ai_response,
                    confidence=0.8,
                    learning_score=0.8,
                    context_requirements=context
                )
                self.adaptive_responses[pattern_key] = adaptive_response
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri pojačavanju uspešnog obrasca: {e}")
    
    def _learn_from_failure(self, user_input: str, ai_response: str, context: Dict[str, Any]):
        """Uči iz neuspeha"""
        try:
            pattern_key = self._extract_pattern_key(user_input)
            
            # Smanji confidence postojećeg pravila
            if pattern_key in self.learning_rules:
                rule = self.learning_rules[pattern_key]
                rule.success_rate = max(0.1, rule.success_rate - 0.2)
                rule.last_used = datetime.now()
            
            # Kreiraj alternativno pravilo
            alternative_rule = LearningRule(
                id=f"rule_alt_{len(self.learning_rules)}",
                condition=f"user_input_contains_{pattern_key}_alternative",
                action="provide_alternative_response",
                priority=0.6,
                success_rate=0.5,
                usage_count=1,
                last_used=datetime.now(),
                created=datetime.now(),
                context=context
            )
            self.learning_rules[alternative_rule.id] = alternative_rule
            
            self.logger.info(f"🔄 Kreirano alternativno pravilo za pattern: {pattern_key}")
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri učenju iz neuspeha: {e}")
    
    def _extract_pattern_key(self, user_input: str) -> str:
        """Izvlači ključ obrasca iz korisničkog unosa"""
        try:
            # Jednostavna ekstrakcija ključnih reči
            input_lower = user_input.lower()
            
            # Ključne reči za kategorizaciju
            patterns = {
                'earning': ['zarada', 'zaradim', 'novac', 'para', 'profit'],
                'platforms': ['platforma', 'platforme', 'sajt', 'sajtovi', 'aplikacija'],
                'technical': ['kako', 'problem', 'greška', 'error', 'ne radi'],
                'emotional': ['frustriran', 'teško', 'problem', 'pomoć', 'pomozi'],
                'general': ['šta', 'koje', 'gde', 'kada', 'zašto']
            }
            
            for pattern, keywords in patterns.items():
                if any(keyword in input_lower for keyword in keywords):
                    return pattern
            
            return 'general'
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri ekstrakciji pattern key-a: {e}")
            return 'general'
    
    def _update_user_behavior(self, feedback: Dict[str, Any]):
        """Ažurira ponašanje korisnika"""
        try:
            user_id = feedback.get('user_id', 'default')
            behavior_type = feedback.get('behavior_type', 'interaction')
            
            if user_id not in self.user_behaviors:
                behavior = UserBehavior(
                    user_id=user_id,
                    behavior_type=behavior_type,
                    frequency=1,
                    last_occurrence=datetime.now(),
                    context=feedback.get('context', {}),
                    satisfaction_history=[feedback.get('satisfaction', 0.5)]
                )
                self.user_behaviors[user_id] = behavior
            else:
                behavior = self.user_behaviors[user_id]
                behavior.frequency += 1
                behavior.last_occurrence = datetime.now()
                behavior.satisfaction_history.append(feedback.get('satisfaction', 0.5))
                
                # Zadrži samo poslednjih 10 satisfaction vrednosti
                if len(behavior.satisfaction_history) > 10:
                    behavior.satisfaction_history = behavior.satisfaction_history[-10:]
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri ažuriranju user behavior-a: {e}")
    
    def generate_adaptive_response(self, user_input: str, context: Dict[str, Any]) -> str:
        """Generiše adaptivni odgovor na osnovu učenja"""
        try:
            # Analiziraj input i pronađi najbolji odgovor
            pattern_key = self._extract_pattern_key(user_input)
            
            # Prvo pokušaj da pronađeš adaptivni odgovor
            if pattern_key in self.adaptive_responses:
                response = self.adaptive_responses[pattern_key]
                
                # Proveri da li odgovor odgovara kontekstu
                if self._context_matches(response.context_requirements, context):
                    # Ažuriraj learning score
                    response.learning_score = min(1.0, response.learning_score + 0.1)
                    return response.response
            
            # Ako nema adaptivnog odgovora, koristi learning rules
            best_rule = self._find_best_rule(user_input, context)
            if best_rule:
                return self._execute_rule(best_rule, context)
            
            # Fallback na generički odgovor
            return self._generate_fallback_response(user_input, context)
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri generisanju adaptivnog odgovora: {e}")
            return "Izvinjavam se, došlo je do greške u AI učenju."
    
    def _context_matches(self, requirements: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Proverava da li kontekst odgovara zahtevima"""
        try:
            for key, required_value in requirements.items():
                if key in context:
                    context_value = context[key]
                    
                    # Jednostavna provera
                    if isinstance(required_value, str):
                        if required_value not in str(context_value).lower():
                            return False
                    elif isinstance(required_value, (int, float)):
                        if context_value != required_value:
                            return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri proveri konteksta: {e}")
            return False
    
    def _find_best_rule(self, user_input: str, context: Dict[str, Any]) -> Optional[LearningRule]:
        """Pronalazi najbolje pravilo za input"""
        try:
            best_rule = None
            best_score = 0.0
            
            for rule in self.learning_rules.values():
                score = self._calculate_rule_score(rule, user_input, context)
                if score > best_score:
                    best_score = score
                    best_rule = rule
            
            return best_rule if best_score > 0.5 else None
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri pronalaženju najboljeg pravila: {e}")
            return None
    
    def _calculate_rule_score(self, rule: LearningRule, user_input: str, context: Dict[str, Any]) -> float:
        """Računa skor pravila"""
        try:
            score = 0.0
            
            # Prioritet pravila
            score += rule.priority * 0.4
            
            # Success rate
            score += rule.success_rate * 0.3
            
            # Kontekstualna relevantnost
            context_match = self._context_matches(rule.context, context)
            if context_match:
                score += 0.2
            
            # Frekvencija korišćenja (normalizovana)
            usage_score = min(rule.usage_count / 10.0, 1.0)
            score += usage_score * 0.1
            
            return score
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri računanju rule score-a: {e}")
            return 0.0
    
    def _execute_rule(self, rule: LearningRule, context: Dict[str, Any]) -> str:
        """Izvršava pravilo i generiše odgovor"""
        try:
            # Ažuriraj statistiku pravila
            rule.usage_count += 1
            rule.last_used = datetime.now()
            
            # Generiši odgovor na osnovu akcije
            if rule.action == "provide_detailed_earning_strategy":
                return self._generate_earning_strategy(context)
            elif rule.action == "list_platforms_with_analysis":
                return self._generate_platform_analysis(context)
            elif rule.action == "provide_emotional_support_and_solutions":
                return self._generate_emotional_support(context)
            elif rule.action == "provide_step_by_step_technical_guidance":
                return self._generate_technical_guidance(context)
            else:
                return self._generate_generic_response(rule, context)
                
        except Exception as e:
            self.logger.error(f"❌ Greška pri izvršavanju pravila: {e}")
            return "Izvinjavam se, došlo je do greške pri izvršavanju pravila."
    
    def _generate_earning_strategy(self, context: Dict[str, Any]) -> str:
        """Generiše strategiju za zaradu"""
        return """🎯 **AI-Generisana Strategija za Zaradu:**

🚀 **Napredni pristup sa AI optimizacijom:**

1. **Smart Diversifikacija:**
   • Koristite 12-15 platformi istovremeno
   • AI automatski balansira aktivnost
   • Fokus na platforme sa ROI > 300%

2. **Vremenska Optimizacija:**
   • AI analizira najprofitabilne časove
   • Automatska adaptacija radnih procesa
   • Predviđanje tržišnih trendova

3. **AI-Enhanced Reputacija:**
   • Automatsko praćenje kvaliteta rada
   • Predviđanje potreba za radnicima
   • Strategijsko planiranje karijere

4. **Napredne Automatizacije:**
   • Smart workflow management
   • Inteligentno balansiranje zadataka
   • Prediktivna analiza tržišta

💡 **AI Preporučujem:** Aktivirajte "Quantum Mode" + "AI Supremacy" za maksimalnu zaradu!"""
    
    def _generate_platform_analysis(self, context: Dict[str, Any]) -> str:
        """Generiše analizu platformi"""
        return """🏆 **AI Analiza Platformi - Real-time:**

📊 **Top Platforme (AI-optimizovano):**

**🥇 Premium Tier:**
• **Textbroker** - $20-80/članak (AI-optimizovano)
• **Upwork** - $30-150/sat (Smart matching)
• **Fiverr** - $10-1000/projekat (Viral potential)

**🥈 Advanced Tier:**
• **Freelancer** - $20-100/sat
• **Guru** - $30-120/sat
• **PeoplePerHour** - $25-90/sat

**🥉 Growth Tier:**
• **Fiverr** - $5-50/projekat
• **Upwork** - $15-50/sat
• **Freelancer** - $10-40/sat

🚀 **AI Preporučujem:** Započnite sa Textbroker + Upwork kombinacijom za maksimalnu zaradu!"""
    
    def _generate_emotional_support(self, context: Dict[str, Any]) -> str:
        """Generiše emocionalnu podršku"""
        return """💙 **AI Emocionalna Podrška:**

🤗 **Razumem vašu frustraciju i tu sam da pomognem:**

**🎯 Trenutni Plan Akcije:**
1. **Identifikujemo problem** - Hajde da ga rešimo korak po korak
2. **Analiziramo situaciju** - AI će dati najbolje rešenje
3. **Implementiramo rešenje** - Pratimo progres zajedno
4. **Optimizujemo rezultate** - Postižemo maksimalan uspeh

**💡 AI Savet:**
• Svaki problem je prilika za učenje
• AI je tu da vam pomogne 24/7
• Zajedno ćemo postići vaše ciljeve

**🚀 Sledeći korak:** Recite mi šta vas konkretno frustrira i AI će dati precizno rešenje!"""
    
    def _generate_technical_guidance(self, context: Dict[str, Any]) -> str:
        """Generiše tehničko uputstvo"""
        return """🔧 **AI Tehničko Uputstvo:**

📋 **Korak-po-Korak Rešenje:**

**1. Diagnostika Problema:**
   • AI analizira trenutno stanje
   • Identifikuje root cause
   • Predlaže optimalno rešenje

**2. Implementacija Rešenja:**
   • Detaljne instrukcije
   • Screenshot tutoriali
   • Video demonstracije

**3. Verifikacija Rešenja:**
   • Testiranje funkcionalnosti
   • Provera performansi
   • Optimizacija ako je potrebno

**4. Preventivne Mere:**
   • AI monitoring
   • Automatske backup-e
   • Prediktivno održavanje

💡 **AI Preporučujem:** Započnite sa detaljnom analizom problema!"""
    
    def _generate_generic_response(self, rule: LearningRule, context: Dict[str, Any]) -> str:
        """Generiše generički odgovor"""
        return f"""🤖 **AI Odgovor (Rule: {rule.action}):**

📚 **Na osnovu AI učenja i analize:**

{rule.condition.replace('_', ' ').title()}

**💡 AI Insight:**
• Ovo pravilo ima {rule.success_rate:.1%} uspešnost
• Korišćeno {rule.usage_count} puta
• Prioritet: {rule.priority:.1%}

**🎯 Sledeći korak:** Recite mi više detalja da bih dao precizniji odgovor!"""
    
    def _generate_fallback_response(self, user_input: str, context: Dict[str, Any]) -> str:
        """Generiše fallback odgovor"""
        return f"""🤖 **AI Fallback Odgovor:**

📝 **Analiziram vaš upit: "{user_input}"**

**🧠 AI Inteligencija:**
• Trenutno nemam dovoljno informacija za precizan odgovor
• AI sistem uči iz svake interakcije
• Vaš upit će biti analiziran za buduće poboljšanje

**💡 Preporučujem:**
• Pokušajte da formulišete pitanje drugačije
• Koristite specifičnije termine
• AI će se prilagoditi vašem stilu komunikacije

**🚀 AI Učenje:** Svaki upit pomaže da postanem pametniji!"""
    
    def _update_learning_metrics(self):
        """Ažurira learning metrike"""
        try:
            total_rules = len(self.learning_rules)
            total_responses = len(self.adaptive_responses)
            
            if total_rules > 0:
                avg_confidence = sum(rule.success_rate for rule in self.learning_rules.values()) / total_rules
                self.learning_metrics['average_confidence'] = avg_confidence
            
            # Računaj learning speed
            recent_rules = [rule for rule in self.learning_rules.values() 
                          if (datetime.now() - rule.created).days < 7]
            self.learning_metrics['learning_speed'] = len(recent_rules) / 7.0  # rules per day
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri ažuriranju learning metrika: {e}")
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Vraća statistiku učenja"""
        try:
            stats = {
                'total_rules': len(self.learning_rules),
                'total_responses': len(self.adaptive_responses),
                'total_behaviors': len(self.user_behaviors),
                'learning_metrics': self.learning_metrics.copy(),
                'recent_activity': {
                    'rules_created_today': len([r for r in self.learning_rules.values() 
                                              if (datetime.now() - r.created).days == 0]),
                    'rules_used_today': len([r for r in self.learning_rules.values() 
                                           if (datetime.now() - r.last_used).days == 0])
                }
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri dohvatanju learning statistike: {e}")
            return {"error": str(e)}
    
    def add_learning_request(self, request: Dict[str, Any]):
        """Dodaje learning zahtev u queue"""
        try:
            self.learning_queue.put(request)
            self.logger.debug(f"📝 Learning zahtev dodat u queue: {request.get('type')}")
        except Exception as e:
            self.logger.error(f"❌ Greška pri dodavanju learning zahteva: {e}")
    
    def shutdown(self):
        """Zaustavlja learning sistem"""
        try:
            self.is_learning = False
            if self.learning_thread and self.learning_thread.is_alive():
                self.learning_thread.join(timeout=5)
            self.logger.info("🛑 Dynamic Learning System zaustavljen")
        except Exception as e:
            self.logger.error(f"❌ Greška pri zaustavljanju: {e}")

# Globalna instanca
dynamic_learning_system = None

def get_dynamic_learning_system() -> DynamicLearningSystem:
    """Vraća globalnu instancu Dynamic Learning System-a"""
    global dynamic_learning_system
    if dynamic_learning_system is None:
        dynamic_learning_system = DynamicLearningSystem()
    return dynamic_learning_system
