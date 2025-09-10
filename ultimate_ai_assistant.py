#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - Ultimate AI Assistant
Napredni AI asistent za AutoEarnPro 2.0
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

class AIStatus(Enum):
    """AI status"""
    IDLE = "idle"
    THINKING = "thinking"
    PROCESSING = "processing"
    LEARNING = "learning"
    ERROR = "error"

@dataclass
class AIRequest:
    """AI request structure"""
    request_id: str
    request_type: str
    prompt: str
    context: Optional[Dict[str, Any]] = None
    priority: str = "normal"
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class AIResponse:
    """AI response structure"""
    request_id: str
    success: bool
    response: str
    confidence: float
    processing_time: float
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class UltimateAIAssistant:
    """Ultimate AI Assistant for AutoEarnPro 2.0"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # AI state
        self.status = AIStatus.IDLE
        self.request_queue: List[AIRequest] = []
        self.response_history: List[AIResponse] = []
        self.learning_data: Dict[str, Any] = {}
        
        # Threading
        self.processing_thread = None
        self.running = False
        self._lock = threading.RLock()
        
        # Callbacks
        self.response_callbacks: List[Callable[[AIResponse], None]] = []
        self.status_callbacks: List[Callable[[AIStatus], None]] = []
        
        # AI capabilities
        self.capabilities = {
            'content_generation': True,
            'task_optimization': True,
            'platform_analysis': True,
            'earning_strategies': True,
            'risk_assessment': True,
            'automation_suggestions': True,
            'code_generation': True,
            'gui_creation': True,
            'api_development': True,
            'data_processing': True
        }
        
        # Initialize Code Generation Engine
        try:
            from .code_generation_engine import get_code_generation_engine
            self.code_engine = get_code_generation_engine()
            self.logger.info("🛠️ Code Generation Engine initialized")
        except ImportError as e:
            self.code_engine = None
            self.logger.warning(f"⚠️ Code Generation Engine not available: {e}")
        
        self.logger.info("🤖 Ultimate AI Assistant initialized")
    
    def chat(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Chat with AI assistant - direct response method"""
        try:
            # Simple chat processing without queuing
            if not message.strip():
                return "Molim vas unesite poruku."
            
            # Process message based on content
            message_lower = message.lower()
            
            # Code generation requests
            if any(word in message_lower for word in ['kodiraj', 'napravi', 'generiši', 'kreiraj', 'gui', 'prozor', 'api', 'skripta']):
                return self._handle_code_generation_request(message, context)
            
            # Platform-related questions
            if any(word in message_lower for word in ['platform', 'platforma', 'zarada', 'zaradu', 'zaraditi']):
                return self._chat_platform_advice(message)
            
            # Account-related questions
            elif any(word in message_lower for word in ['nalog', 'account', 'email', 'gmail', 'kreirati', 'dodati']):
                return self._chat_account_advice(message)
            
            # Payment-related questions
            elif any(word in message_lower for word in ['isplata', 'paypal', 'payoneer', 'skrill', 'crypto', 'kripto']):
                return self._chat_payment_advice(message)
            
            # General help
            elif any(word in message_lower for word in ['pomoć', 'pomoc', 'help', 'kako', 'šta', 'sta']):
                return self._chat_general_help(message)
            
            # Default response
            else:
                return self._chat_generic_response(message)
                
        except Exception as e:
            self.logger.error(f"Error in chat: {e}")
            return f"Greška u AI asistentu: {e}"
    
    def submit_request(self, request_type: str, prompt: str, context: Optional[Dict[str, Any]] = None, priority: str = "normal") -> str:
        """Submit a request to the AI assistant"""
        try:
            request_id = f"ai_req_{int(time.time())}_{random.randint(1000, 9999)}"
            
            request = AIRequest(
                request_id=request_id,
                request_type=request_type,
                prompt=prompt,
                context=context,
                priority=priority
            )
            
            with self._lock:
                self.request_queue.append(request)
                
                # Sort by priority
                self.request_queue.sort(key=lambda x: {"high": 0, "normal": 1, "low": 2}.get(x.priority, 1))
            
            self.logger.info(f"AI request submitted: {request_id} ({request_type})")
            
            # Start processing if not already running
            if not self.running:
                self._start_processing()
            
            return request_id
            
        except Exception as e:
            self.logger.error(f"Error submitting AI request: {e}")
            return ""
    
    def get_response(self, request_id: str) -> Optional[AIResponse]:
        """Get response for a specific request"""
        try:
            with self._lock:
                for response in self.response_history:
                    if response.request_id == request_id:
                        return response
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting AI response: {e}")
            return None
    
    def add_response_callback(self, callback: Callable[[AIResponse], None]):
        """Add response callback"""
        self.response_callbacks.append(callback)
    
    def add_status_callback(self, callback: Callable[[AIStatus], None]):
        """Add status callback"""
        self.status_callbacks.append(callback)
    
    def _start_processing(self):
        """Start AI processing thread"""
        if self.running:
            return
        
        self.running = True
        self.processing_thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.processing_thread.start()
        
        self.logger.info("AI processing started")
    
    def _processing_loop(self):
        """Main AI processing loop"""
        while self.running:
            try:
                # Get next request
                request = None
                with self._lock:
                    if self.request_queue:
                        request = self.request_queue.pop(0)
                
                if request:
                    self._process_request(request)
                else:
                    time.sleep(1)
                    
            except Exception as e:
                self.logger.error(f"Error in AI processing loop: {e}")
                time.sleep(5)
    
    def _process_request(self, request: AIRequest):
        """Process a single AI request"""
        start_time = time.time()
        
        try:
            # Update status
            self._update_status(AIStatus.PROCESSING)
            
            # Process based on request type
            if request.request_type == "content_generation":
                response = self._generate_content(request)
            elif request.request_type == "task_optimization":
                response = self._optimize_task(request)
            elif request.request_type == "platform_analysis":
                response = self._analyze_platform(request)
            elif request.request_type == "earning_strategies":
                response = self._suggest_earning_strategies(request)
            elif request.request_type == "risk_assessment":
                response = self._assess_risk(request)
            elif request.request_type == "automation_suggestions":
                response = self._suggest_automation(request)
            else:
                response = self._generic_processing(request)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Create response
            ai_response = AIResponse(
                request_id=request.request_id,
                success=response.get('success', False),
                response=response.get('response', ''),
                confidence=response.get('confidence', 0.0),
                processing_time=processing_time,
                metadata=response.get('metadata')
            )
            
            # Add to history
            with self._lock:
                self.response_history.append(ai_response)
                
                # Keep history manageable
                if len(self.response_history) > 1000:
                    self.response_history = self.response_history[-1000:]
            
            # Notify callbacks
            self._notify_response_callbacks(ai_response)
            
            # Update status
            self._update_status(AIStatus.IDLE)
            
            self.logger.info(f"AI request processed: {request.request_id}")
            
        except Exception as e:
            self.logger.error(f"Error processing AI request {request.request_id}: {e}")
            self._update_status(AIStatus.ERROR)
    
    def _generate_content(self, request: AIRequest) -> Dict[str, Any]:
        """Generate content based on request"""
        # Simulate content generation
        time.sleep(random.uniform(1, 3))
        
        content_types = {
            'article': 'Detaljan članak o temi',
            'blog_post': 'Blog post sa praktičnim savetima',
            'product_description': 'Opis proizvoda sa ključnim karakteristikama',
            'social_media': 'Kratak i angažovan sadržaj za društvene mreže'
        }
        
        content_type = request.context.get('content_type', 'article') if request.context else 'article'
        base_content = content_types.get(content_type, 'Generisan sadržaj')
        
        return {
            'success': True,
            'response': f"{base_content}: {request.prompt}",
            'confidence': random.uniform(0.7, 0.95),
            'metadata': {
                'content_type': content_type,
                'word_count': random.randint(200, 1000),
                'seo_optimized': True
            }
        }
    
    def _optimize_task(self, request: AIRequest) -> Dict[str, Any]:
        """Optimize task execution"""
        time.sleep(random.uniform(0.5, 2))
        
        return {
            'success': True,
            'response': f"Optimizovana strategija za: {request.prompt}",
            'confidence': random.uniform(0.8, 0.95),
            'metadata': {
                'optimization_type': 'task_efficiency',
                'estimated_improvement': f"{random.randint(10, 50)}%"
            }
        }
    
    def _analyze_platform(self, request: AIRequest) -> Dict[str, Any]:
        """Analyze platform performance"""
        time.sleep(random.uniform(1, 2))
        
        return {
            'success': True,
            'response': f"Analiza platforme: {request.prompt}",
            'confidence': random.uniform(0.75, 0.9),
            'metadata': {
                'analysis_type': 'performance_metrics',
                'recommendations_count': random.randint(3, 8)
            }
        }
    
    def _suggest_earning_strategies(self, request: AIRequest) -> Dict[str, Any]:
        """Suggest earning strategies"""
        time.sleep(random.uniform(1, 3))
        
        strategies = [
            "Fokus na visoko-plaćene kategorije",
            "Diverzifikacija platformi",
            "Optimizacija vremena rada",
            "Kvalitet nad kvantitetom",
            "Automatska optimizacija"
        ]
        
        return {
            'success': True,
            'response': f"Strategije za zaradu: {', '.join(random.sample(strategies, 3))}",
            'confidence': random.uniform(0.8, 0.95),
            'metadata': {
                'strategies_count': 3,
                'estimated_earnings_increase': f"{random.randint(15, 40)}%"
            }
        }
    
    def _assess_risk(self, request: AIRequest) -> Dict[str, Any]:
        """Assess risk level"""
        time.sleep(random.uniform(0.5, 1.5))
        
        risk_levels = ['Nizak', 'Srednji', 'Visok']
        selected_risk = random.choice(risk_levels)
        
        return {
            'success': True,
            'response': f"Procena rizika: {selected_risk} - {request.prompt}",
            'confidence': random.uniform(0.7, 0.9),
            'metadata': {
                'risk_level': selected_risk,
                'mitigation_suggestions': random.randint(2, 5)
            }
        }
    
    def _suggest_automation(self, request: AIRequest) -> Dict[str, Any]:
        """Suggest automation improvements"""
        time.sleep(random.uniform(1, 2))
        
        automation_suggestions = [
            "Automatizacija prijave na platforme",
            "Auto-generisanje sadržaja",
            "Inteligentno planiranje zadataka",
            "Automatsko praćenje zarade",
            "Smart notifikacije"
        ]
        
        return {
            'success': True,
            'response': f"Automatske preporuke: {', '.join(random.sample(automation_suggestions, 2))}",
            'confidence': random.uniform(0.75, 0.9),
            'metadata': {
                'automation_areas': 2,
                'time_savings': f"{random.randint(20, 60)}%"
            }
        }
    
    def _generic_processing(self, request: AIRequest) -> Dict[str, Any]:
        """Generic AI processing"""
        time.sleep(random.uniform(1, 3))
        
        return {
            'success': True,
            'response': f"AI analiza: {request.prompt}",
            'confidence': random.uniform(0.6, 0.85),
            'metadata': {
                'processing_type': 'generic',
                'ai_model': 'AutoEarnPro_AI_v2.0'
            }
        }
    
    def _update_status(self, status: AIStatus):
        """Update AI status"""
        self.status = status
        self._notify_status_callbacks(status)
    
    def _notify_response_callbacks(self, response: AIResponse):
        """Notify response callbacks"""
        for callback in self.response_callbacks:
            try:
                callback(response)
            except Exception as e:
                self.logger.error(f"Error in response callback: {e}")
    
    def _notify_status_callbacks(self, status: AIStatus):
        """Notify status callbacks"""
        for callback in self.status_callbacks:
            try:
                callback(status)
            except Exception as e:
                self.logger.error(f"Error in status callback: {e}")
    
    def get_status(self) -> AIStatus:
        """Get current AI status"""
        return self.status
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get AI statistics"""
        with self._lock:
            total_requests = len(self.response_history)
            successful_requests = len([r for r in self.response_history if r.success])
            failed_requests = total_requests - successful_requests
            
            avg_processing_time = sum(r.processing_time for r in self.response_history) / total_requests if total_requests > 0 else 0
            avg_confidence = sum(r.confidence for r in self.response_history) / total_requests if total_requests > 0 else 0
            
            return {
                'total_requests': total_requests,
                'successful_requests': successful_requests,
                'failed_requests': failed_requests,
                'success_rate': (successful_requests / total_requests * 100) if total_requests > 0 else 0,
                'avg_processing_time': avg_processing_time,
                'avg_confidence': avg_confidence,
                'pending_requests': len(self.request_queue),
                'status': self.status.value
            }
    
    def _chat_platform_advice(self, message: str) -> str:
        """Provide platform-related advice"""
        advice = [
            "🚀 **Najbolje platforme za zaradu:**",
            "• **Textbroker** - Pisanje članaka (€2-€50 po članku)",
            "• **iWriter** - Content creation ($2.15-$84 po članku)",
            "• **Survey Junkie** - Ankete ($1-$50 po anketi)",
            "• **Swagbucks** - Razne aktivnosti ($1-$100 dnevno)",
            "• **Amazon MTurk** - Mikro-zadaci ($0.01-$20 po zadatku)",
            "• **Upwork** - Freelancing ($5-$500+ po projektu)",
            "• **Fiverr** - Gig-based ($5-$1000+ po gig-u)",
            "",
            "💡 **Savet:** Fokusirajte se na 3-5 platforme koje vam najviše odgovaraju!"
        ]
        return "\n".join(advice)
    
    def _chat_account_advice(self, message: str) -> str:
        """Provide account-related advice"""
        advice = [
            "👤 **Kreiranje naloga:**",
            "• Koristite dugme '👤 Dodaj Nalog' za automatsko kreiranje",
            "• Program automatski kreira Gmail adresu sa random imenom",
            "• Generiše sigurnu lozinku sa specijalnim karakterima",
            "• Kreira naloge na 35+ platformama automatski",
            "",
            "📧 **Ručno dodavanje:**",
            "• Koristite dugme '📧 Dodaj Email' za ručno unosenje",
            "• Unesite svoj email i lozinku",
            "• Program će kreirati naloge na svim platformama",
            "",
            "🔒 **Sigurnost:**",
            "• Svaki nalog ima jedinstvenu lozinku",
            "• Lozinke se generišu sa specijalnim karakterima",
            "• Nalozi se čuvaju lokalno u memoriji"
        ]
        return "\n".join(advice)
    
    def _chat_payment_advice(self, message: str) -> str:
        """Provide payment-related advice"""
        advice = [
            "💰 **Strategija isplata:**",
            "• **Crypto Accounts** - Glavni način za Scripted, HackerRank",
            "• **Check** - Glavni način za Pinecone Research",
            "• **PayPal** - Maksimalno $2500 mesečno",
            "• **Skrill & Payoneer** - Raspoređuje se ostatak",
            "",
            "🎯 **Prioriteti:**",
            "1. Crypto Accounts (gde je glavni način)",
            "2. Check (gde je glavni način)",
            "3. Payoneer, Skrill, Wise",
            "4. Bank Transfer, SEPA",
            "5. PayPal (samo ako nema drugih opcija)",
            "",
            "💡 **Koristite Payout Strategy tab za detaljnu konfiguraciju!**"
        ]
        return "\n".join(advice)
    
    def _chat_general_help(self, message: str) -> str:
        """Provide general help"""
        help_text = [
            "🤖 **AI Asistent - Pomoć:**",
            "",
            "🎯 **Glavne funkcionalnosti:**",
            "• **👤 Dodaj Nalog** - Automatsko kreiranje naloga na svim platformama",
            "• **📧 Dodaj Email** - Ručno dodavanje email-a i kreiranje naloga",
            "• **➕ Master Nalog** - Kreiranje master naloga sa dodatnim opcijama",
            "• **💰 Isplate** - Upravljanje isplatama i strategijama",
            "• **📊 Monitor** - Praćenje performansi i zarade",
            "• **🚀 Napredne Funkcije** - AI, analitika, automatizacija",
            "",
            "💬 **Kako koristiti AI Asistent:**",
            "• Pitajte o platformama, zaradi, nalozima, isplatama",
            "• AI će vam dati detaljne savete i preporuke",
            "• Koristite srpski ili engleski jezik",
            "",
            "🔧 **Potrebna pomoć?** Pitajte bilo šta!"
        ]
        return "\n".join(help_text)
    
    def _chat_generic_response(self, message: str) -> str:
        """Provide generic response for unknown queries"""
        responses = [
            f"🤖 **AI Asistent:** Hvala na pitanju! '{message}' je odlično pitanje.",
            "",
            "💡 **Mogu vam pomoći sa:**",
            "• Savetima o platformama i zaradi",
            "• Kreiranjem i upravljanjem nalozima",
            "• Strategijama isplata",
            "• Optimizacijom rada",
            "• Automatizacijom procesa",
            "",
            "🎯 **Pokušajte da pitate:**",
            "• 'Kako da zaradim više?'",
            "• 'Koje su najbolje platforme?'",
            "• 'Kako da kreiram naloge?'",
            "• 'Kako funkcioniše isplata?'",
            "",
            "🚀 **AI Asistent je tu da vam pomogne!**"
        ]
        return "\n".join(responses)
    
    def shutdown(self):
        """Shutdown AI assistant"""
        try:
            self.running = False
            
            if self.processing_thread:
                self.processing_thread.join(timeout=5)
            
            self._update_status(AIStatus.IDLE)
            self.logger.info("🔒 Ultimate AI Assistant shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during AI shutdown: {e}")
    
    def _handle_code_generation_request(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Handle code generation requests"""
        try:
            if not self.code_engine:
                return "❌ Code Generation Engine nije dostupan. Molim vas proverite instalaciju."
            
            # Get code suggestions based on user request
            suggestions = self.code_engine.get_code_suggestions(message)
            
            if not suggestions:
                return "❌ Ne mogu da pronađem odgovarajući template za vaš zahtev. Molim vas budite specifičniji."
            
            # Show available templates
            response = "🛠️ **Code Generation - Dostupni Template-i:**\n\n"
            
            for i, template in enumerate(suggestions[:3], 1):
                response += f"**{i}. {template.name}**\n"
                response += f"   📝 {template.description}\n"
                response += f"   🏷️ Kategorija: {template.category}\n"
                response += f"   💡 Primer: {template.examples[0] if template.examples else 'N/A'}\n\n"
            
            response += "**Da generišem kod, recite mi:**\n"
            response += "• Koji template želite (broj 1-3)\n"
            response += "• Koje parametre treba da postavim\n"
            response += "• Gde da sačuvam generisani kod\n\n"
            
            response += "**Primer:** 'Koristi template 1 sa parametrima: window_name=Korisnici, class_name=UserManager, window_size=800x600'"
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Error in code generation request: {e}")
            return f"Greška pri obradi zahteva za generisanje koda: {e}"
    
    def generate_code(self, template_id: str, parameters: Dict[str, Any], save_path: str = None) -> str:
        """Generate code using specified template and parameters"""
        try:
            if not self.code_engine:
                return "❌ Code Generation Engine nije dostupan."
            
            # Generate code
            generated_code = self.code_engine.generate_code(template_id, parameters, "User request")
            
            if not generated_code:
                return "❌ Greška pri generisanju koda. Proverite parametre."
            
            # Save code if path provided
            if save_path:
                if self.code_engine.save_generated_code(generated_code.id, save_path):
                    response = f"✅ **Kod uspešno generisan i sačuvan u:** `{save_path}`\n\n"
                else:
                    response = "⚠️ **Kod generisan ali nije sačuvan.**\n\n"
            else:
                response = "✅ **Kod uspešno generisan:**\n\n"
            
            # Analyze code
            analysis = self.code_engine.analyze_code(generated_code.id)
            if analysis:
                response += f"📊 **Analiza koda:**\n"
                response += f"   • Linije: {analysis.line_count}\n"
                response += f"   • Funkcije: {analysis.function_count}\n"
                response += f"   • Klase: {analysis.class_count}\n"
                response += f"   • Sintaksa: {'✅ Validna' if analysis.syntax_valid else '❌ Greška'}\n\n"
                
                if analysis.suggestions:
                    response += "💡 **Predlozi za poboljšanje:**\n"
                    for suggestion in analysis.suggestions:
                        response += f"   • {suggestion}\n"
                    response += "\n"
            
            response += "**Generisani kod je spreman za korišćenje!** 🚀"
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Error in code generation: {e}")
            return f"Greška pri generisanju koda: {e}"

# Global AI assistant instance
_global_ai_assistant = None

def get_ultimate_ai_assistant(config: Optional[Dict[str, Any]] = None) -> UltimateAIAssistant:
    """Get global AI assistant instance"""
    global _global_ai_assistant
    if _global_ai_assistant is None:
        _global_ai_assistant = UltimateAIAssistant(config)
    return _global_ai_assistant
