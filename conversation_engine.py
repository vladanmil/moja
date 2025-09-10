#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - Advanced Conversation Engine
Omogućava prirodan razgovor sa AI Asistentom
"""

import logging
import json
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from .nlp_engine import NLPResult, QuestionType, QuestionIntent
from .ai_hub import AIHub

logger = logging.getLogger(__name__)

@dataclass
class ConversationContext:
    """Kontekst konverzacije"""
    user_id: str
    session_start: datetime
    conversation_history: List[Dict[str, Any]]
    user_preferences: Dict[str, Any]
    current_topic: str
    mood: str
    expertise_level: str
    last_interaction: datetime

@dataclass
class ConversationResponse:
    """Odgovor u konverzaciji"""
    text: str
    confidence: float
    context_aware: bool
    personalized: bool
    follow_up_questions: List[str]
    suggested_actions: List[str]
    emotional_tone: str

class AdvancedConversationEngine:
    """Napredni engine za prirodan razgovor"""
    
    def __init__(self, ai_hub: AIHub):
        self.logger = logging.getLogger(__name__)
        self.ai_hub = ai_hub
        
        # Konverzacijski kontekst
        self.conversations: Dict[str, ConversationContext] = {}
        
        # Napredni response template-i
        self.response_templates = self._load_response_templates()
        
        # Konverzacijske strategije
        self.conversation_strategies = self._load_conversation_strategies()
        
        # Emotivni tonovi
        self.emotional_tones = {
            "friendly": ["😊", "😄", "🤗", "💪", "🎉"],
            "professional": ["📊", "🎯", "⚡", "🚀", "💡"],
            "encouraging": ["🌟", "💫", "🔥", "💎", "🏆"],
            "calm": ["🌿", "🍃", "💧", "☁️", "🌅"],
            "excited": ["🚀", "💥", "🔥", "⚡", "🎊"]
        }
        
        self.logger.info("🧠 Advanced Conversation Engine uspešno inicijalizovan")
    
    def _load_response_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """Učitava napredne response template-e"""
        return {
            "greeting": [
                {
                    "pattern": "zdravo|hello|hi|hey|ćao|cao",
                    "responses": [
                        "Zdravo! 🎉 Drago mi je što ste ovde! Kako vam mogu pomoći danas?",
                        "Ćao! 😊 Dobrodošli u AutoEarnPro 2.0! Šta vas zanima?",
                        "Zdravo! 🚀 Spreman sam da vam pomognem sa svim pitanjima o zaradi!"
                    ],
                    "follow_up": ["Kako vam mogu pomoći?", "Šta vas zanima?", "Imate li pitanja?"]
                }
            ],
            "earning_question": [
                {
                    "pattern": "kako.*zaraditi|how.*earn|zarada|money|profit",
                    "responses": [
                        "Odlično pitanje! 💰 Imam nekoliko AI-optimizovanih strategija za vas:",
                        "Earning AI je ovde da vam pomogne! 🎯 Evo najboljih strategija:",
                        "Zarada je moja specijalnost! 🚀 Hajde da analiziramo vaše opcije:"
                    ],
                    "follow_up": ["Koju platformu preferirate?", "Koliko vremena imate?", "Koji je vaš cilj?"]
                }
            ],
            "platform_question": [
                {
                    "pattern": "platforme|platforms|sajt|website|app",
                    "responses": [
                        "Platforme su ključne za zaradu! 🏆 AI analizira sve opcije:",
                        "Imam detaljnu analizu platformi! 📊 Evo najboljih izbora:",
                        "Platforme su moja ekspertiza! 🎯 Hajde da pronađemo najbolje za vas:"
                    ],
                    "follow_up": ["Koji tip posla preferirate?", "Koliko ste iskusni?", "Koji je vaš proračun?"]
                }
            ],
            "content_question": [
                {
                    "pattern": "sadržaj|content|članak|article|blog|video",
                    "responses": [
                        "Content je kralj! 👑 AI Content Generator je ovde da vam pomogne:",
                        "Sadržaj je moja strast! 🎨 Evo kako da kreirate viral sadržaj:",
                        "Content strategije su ključne! 📝 Hajde da optimizujemo vaš pristup:"
                    ],
                    "follow_up": ["Koju platformu koristite?", "Koji tip sadržaja?", "Koji je vaš cilj?"]
                }
            ],
            "crypto_question": [
                {
                    "pattern": "kripto|crypto|bitcoin|ethereum|trading",
                    "responses": [
                        "Crypto je budućnost! ₿ AI Crypto Engine analizira tržište:",
                        "Crypto trading je moja ekspertiza! 🚀 Evo najboljih strategija:",
                        "Crypto je odličan izbor! 💎 Hajde da analiziramo prilike:"
                    ],
                    "follow_up": ["Koje kriptovalute vas zanimaju?", "Koji je vaš risk tolerance?", "Koji timeframe?"]
                }
            ],
            "technical_question": [
                {
                    "pattern": "problem|greška|error|bug|ne radi|doesn't work",
                    "responses": [
                        "Tehnički problemi su rešivi! 🔧 Hajde da dijagnostikujemo:",
                        "Ne brinite, rešićemo to! 🛠️ AI analiza će pronaći problem:",
                        "Tehnička podrška je ovde! 💪 Hajde da rešimo problem:"
                    ],
                    "follow_up": ["Kada se problem javio?", "Koji sistem koristite?", "Koja je greška?"]
                }
            ],
            "general_question": [
                {
                    "pattern": "šta|what|kako|how|zašto|why",
                    "responses": [
                        "Odlično pitanje! 🤔 AI Hub ima sve odgovore:",
                        "Interesantno! 💭 Hajde da istražimo to zajedno:",
                        "To je dobro pitanje! 🎯 AI analiza će dati odgovor:"
                    ],
                    "follow_up": ["Možete li detaljnije objasniti?", "Koji aspekt vas zanima?", "Imate li specifičan primer?"]
                }
            ]
        }
    
    def _load_conversation_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Učitava konverzacijske strategije"""
        return {
            "beginner": {
                "tone": "friendly",
                "detail_level": "basic",
                "examples": True,
                "step_by_step": True,
                "encouragement": True
            },
            "intermediate": {
                "tone": "professional",
                "detail_level": "moderate",
                "examples": True,
                "step_by_step": False,
                "encouragement": True
            },
            "expert": {
                "tone": "professional",
                "detail_level": "advanced",
                "examples": False,
                "step_by_step": False,
                "encouragement": False
            }
        }
    
    def start_conversation(self, user_id: str = "default") -> ConversationContext:
        """Započinje novu konverzaciju"""
        context = ConversationContext(
            user_id=user_id,
            session_start=datetime.now(),
            conversation_history=[],
            user_preferences={},
            current_topic="general",
            mood="neutral",
            expertise_level="intermediate",
            last_interaction=datetime.now()
        )
        
        self.conversations[user_id] = context
        self.logger.info(f"🚀 Nova konverzacija započeta za korisnika: {user_id}")
        return context
    
    def get_conversation_context(self, user_id: str = "default") -> ConversationContext:
        """Dohvata kontekst konverzacije"""
        if user_id not in self.conversations:
            return self.start_conversation(user_id)
        return self.conversations[user_id]
    
    def generate_conversation_response(self, message: str, user_id: str = "default") -> ConversationResponse:
        """Generiše prirodan odgovor u konverzaciji"""
        try:
            # Dohvata kontekst
            context = self.get_conversation_context(user_id)
            
            # Analizira poruku
            nlp_result = self.ai_hub.modules['nlp_engine'].analyze_text(message)
            
            # Ažurira kontekst
            self._update_conversation_context(context, message, nlp_result)
            
            # Generiše odgovor
            response = self._generate_contextual_response(message, nlp_result, context)
            
            # Dodaje u istoriju
            self._add_to_conversation_history(context, message, response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Greška u generisanju konverzacijskog odgovora: {e}")
            return self._generate_fallback_response(message)
    
    def _update_conversation_context(self, context: ConversationContext, message: str, nlp_result: NLPResult):
        """Ažurira kontekst konverzacije"""
        # Ažurira trenutnu temu
        if nlp_result.question_type != QuestionType.GENERAL:
            context.current_topic = nlp_result.question_type.value
        
        # Ažurira mood
        context.mood = nlp_result.sentiment
        
        # Ažurira poslednju interakciju
        context.last_interaction = datetime.now()
        
        # Analizira ekspertizu korisnika
        context.expertise_level = self._analyze_expertise_level(message, context)
    
    def _analyze_expertise_level(self, message: str, context: ConversationContext) -> str:
        """Analizira nivo ekspertize korisnika"""
        # Analizira kompleksnost pitanja
        word_count = len(message.split())
        has_technical_terms = any(term in message.lower() for term in [
            "api", "integration", "optimization", "algorithm", "workflow", "automation"
        ])
        has_basic_terms = any(term in message.lower() for term in [
            "kako", "šta", "zašto", "gdje", "kada"
        ])
        
        if has_technical_terms and word_count > 15:
            return "expert"
        elif has_basic_terms and word_count < 10:
            return "beginner"
        else:
            return "intermediate"
    
    def _generate_contextual_response(self, message: str, nlp_result: NLPResult, context: ConversationContext) -> ConversationResponse:
        """Generiše kontekstualni odgovor"""
        # Pronalazi najbolji template
        template = self._find_best_response_template(message, nlp_result)
        
        # Generiše osnovni odgovor
        base_response = self._generate_base_response(template, nlp_result, context)
        
        # Personalizuje odgovor
        personalized_response = self._personalize_response(base_response, context)
        
        # Dodaje follow-up pitanja
        follow_up = self._generate_follow_up_questions(template, context)
        
        # Dodaje predložene akcije
        suggested_actions = self._generate_suggested_actions(nlp_result, context)
        
        # Određuje emotivni ton
        emotional_tone = self._determine_emotional_tone(context)
        
        return ConversationResponse(
            text=personalized_response,
            confidence=nlp_result.confidence,
            context_aware=True,
            personalized=True,
            follow_up_questions=follow_up,
            suggested_actions=suggested_actions,
            emotional_tone=emotional_tone
        )
    
    def _find_best_response_template(self, message: str, nlp_result: NLPResult) -> Dict[str, Any]:
        """Pronalazi najbolji response template"""
        message_lower = message.lower()
        
        for category, templates in self.response_templates.items():
            for template in templates:
                if any(pattern in message_lower for pattern in template["pattern"].split("|")):
                    return template
        
        # Fallback template
        return {
            "pattern": "general",
            "responses": ["Interesantno pitanje! 🤔 Kako vam mogu pomoći?"],
            "follow_up": ["Možete li detaljnije objasniti?", "Koji aspekt vas zanima?"]
        }
    
    def _generate_base_response(self, template: Dict[str, Any], nlp_result: NLPResult, context: ConversationContext) -> str:
        """Generiše osnovni odgovor"""
        # Bira random response iz template-a
        base_response = random.choice(template["responses"])
        
        # Dodaje AI Hub informacije ako je potrebno
        if nlp_result.question_type in [QuestionType.EARNING, QuestionType.PLATFORMS, QuestionType.CONTENT]:
            base_response += "\n\n" + self._get_ai_hub_insights(nlp_result.question_type)
        
        return base_response
    
    def _get_ai_hub_insights(self, question_type: QuestionType) -> str:
        """Dohvata AI Hub insights za specifičnu temu"""
        try:
            if question_type == QuestionType.EARNING:
                knowledge = self.ai_hub.get_knowledge('earning_strategies')
                if knowledge:
                    return f"💡 **AI Insight:** {knowledge.description}"
            
            elif question_type == QuestionType.PLATFORMS:
                knowledge = self.ai_hub.get_knowledge('platform_insights')
                if knowledge:
                    return f"💡 **AI Insight:** {knowledge.description}"
            
            elif question_type == QuestionType.CONTENT:
                knowledge = self.ai_hub.get_knowledge('content_creation')
                if knowledge:
                    return f"💡 **AI Insight:** {knowledge.description}"
            
            return ""
            
        except Exception as e:
            self.logger.error(f"Greška pri dohvatanju AI Hub insights: {e}")
            return ""
    
    def _personalize_response(self, response: str, context: ConversationContext) -> str:
        """Personalizuje odgovor na osnovu konteksta"""
        # Dodaje personalizaciju na osnovu ekspertize
        if context.expertise_level == "beginner":
            response += "\n\n🌟 **Za početnike:** Preporučujem da počnete sa osnovama i postepeno napredujete."
        elif context.expertise_level == "expert":
            response += "\n\n🚀 **Za eksperte:** Možete koristiti napredne AI funkcionalnosti za maksimalnu optimizaciju."
        
        # Dodaje personalizaciju na osnovu mood-a
        if context.mood == "positive":
            response += "\n\n😊 **Vidim da ste pozitivno raspoloženi!** To je odlično za uspeh!"
        elif context.mood == "negative":
            response += "\n\n🤗 **Ne brinite!** Zajedno ćemo rešiti sve probleme."
        
        # Dodaje personalizaciju na osnovu teme
        if context.current_topic != "general":
            response += f"\n\n🎯 **Trenutna tema:** {context.current_topic.replace('_', ' ').title()}"
        
        return response
    
    def _generate_follow_up_questions(self, template: Dict[str, Any], context: ConversationContext) -> List[str]:
        """Generiše follow-up pitanja"""
        follow_up = template.get("follow_up", [])
        
        # Dodaje kontekstualna pitanja
        if context.current_topic == "earning":
            follow_up.extend([
                "Koji je vaš cilj zarade?",
                "Koliko vremena možete da posvetite?",
                "Koje platforme već koristite?"
            ])
        elif context.current_topic == "platforms":
            follow_up.extend([
                "Koji tip posla preferirate?",
                "Da li ste spremni za content writing?",
                "Koliko ste iskusni u online zaradi?"
            ])
        
        return follow_up[:3]  # Maksimalno 3 pitanja
    
    def _generate_suggested_actions(self, nlp_result: NLPResult, context: ConversationContext) -> List[str]:
        """Generiše predložene akcije"""
        actions = []
        
        if nlp_result.question_type == QuestionType.EARNING:
            actions.extend([
                "🎯 Analiziraj vaše trenutne platforme",
                "📊 Kreiraj earning strategiju",
                "🚀 Pokreni AI optimizaciju"
            ])
        elif nlp_result.question_type == QuestionType.PLATFORMS:
            actions.extend([
                "🔍 Pretraži najbolje platforme",
                "📱 Kreiraj nove naloge",
                "⚡ Optimizuj postojeće"
            ])
        elif nlp_result.question_type == QuestionType.CONTENT:
            actions.extend([
                "✍️ Generiši content strategiju",
                "🎨 Kreiraj viral sadržaj",
                "📈 Optimizuj za SEO"
            ])
        
        # Dodaje opšte akcije
        actions.extend([
            "🤖 Otvori AI Hub",
            "📚 Pregledaj bazu znanja",
            "💬 Postavi više pitanja"
        ])
        
        return actions[:5]  # Maksimalno 5 akcija
    
    def _determine_emotional_tone(self, context: ConversationContext) -> str:
        """Određuje emotivni ton odgovora"""
        strategy = self.conversation_strategies.get(context.expertise_level, {})
        return strategy.get("tone", "friendly")
    
    def _add_to_conversation_history(self, context: ConversationContext, message: str, response: ConversationResponse):
        """Dodaje u istoriju konverzacije"""
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "ai_response": response.text,
            "confidence": response.confidence,
            "topic": context.current_topic,
            "mood": context.mood
        }
        
        context.conversation_history.append(history_entry)
        
        # Održava istoriju na razumnom nivou (zadnjih 50 poruka)
        if len(context.conversation_history) > 50:
            context.conversation_history = context.conversation_history[-50:]
    
    def _generate_fallback_response(self, message: str) -> ConversationResponse:
        """Generiše fallback odgovor"""
        return ConversationResponse(
            text="Izvinjavam se, imam tehnički problem. Pokušajte ponovo ili koristite 'AI Hub' komandu.",
            confidence=0.0,
            context_aware=False,
            personalized=False,
            follow_up_questions=["Da li možete ponoviti pitanje?"],
            suggested_actions=["🤖 Otvori AI Hub", "🔄 Pokušaj ponovo"],
            emotional_tone="calm"
        )
    
    def get_conversation_summary(self, user_id: str = "default") -> str:
        """Vraća sažetak konverzacije"""
        context = self.get_conversation_context(user_id)
        
        if not context.conversation_history:
            return "Nema istorije konverzacije."
        
        summary = f"""
📊 **Sažetak konverzacije za korisnika: {context.user_id}**

🕐 **Trajanje sesije:** {datetime.now() - context.session_start}
💬 **Broj poruka:** {len(context.conversation_history)}
🎯 **Glavna tema:** {context.current_topic.replace('_', ' ').title()}
😊 **Mood:** {context.mood}
🧠 **Nivo ekspertize:** {context.expertise_level}

**📝 Poslednje poruke:**
"""
        
        # Prikazuje zadnjih 5 poruka
        for entry in context.conversation_history[-5:]:
            summary += f"• **{entry['timestamp'][:16]}:** {entry['user_message'][:50]}...\n"
        
        return summary
    
    def clear_conversation_history(self, user_id: str = "default"):
        """Briše istoriju konverzacije"""
        if user_id in self.conversations:
            self.conversations[user_id].conversation_history.clear()
            self.logger.info(f"🗑️ Istorija konverzacije obrisana za korisnika: {user_id}")

# Globalna instanca Advanced Conversation Engine-a
conversation_engine = None

def get_conversation_engine(ai_hub: AIHub = None) -> AdvancedConversationEngine:
    """Vraća globalnu instancu Advanced Conversation Engine-a"""
    global conversation_engine
    if conversation_engine is None and ai_hub:
        conversation_engine = AdvancedConversationEngine(ai_hub)
    return conversation_engine

def start_conversation(user_id: str = "default", ai_hub: AIHub = None) -> ConversationContext:
    """Brza funkcija za započinjanje konverzacije"""
    engine = get_conversation_engine(ai_hub)
    return engine.start_conversation(user_id)

def generate_response(message: str, user_id: str = "default", ai_hub: AIHub = None) -> ConversationResponse:
    """Brza funkcija za generisanje odgovora"""
    engine = get_conversation_engine(ai_hub)
    return engine.generate_conversation_response(message, user_id)
