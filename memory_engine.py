#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - Memory Engine
Daje AI asistentu pravu memoriju, učenje i inteligenciju
"""

import json
import pickle
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import logging

logger = logging.getLogger(__name__)

@dataclass
class Memory:
    """Pojedinačna memorija"""
    id: str
    content: str
    context: Dict[str, Any]
    timestamp: datetime
    importance: float  # 0.0 - 1.0
    category: str
    tags: List[str]
    access_count: int
    last_accessed: datetime
    emotional_tone: str
    user_satisfaction: float

@dataclass
class ConversationMemory:
    """Memorija konverzacije"""
    user_id: str
    conversation_id: str
    messages: List[Dict[str, Any]]
    context: Dict[str, Any]
    start_time: datetime
    last_activity: datetime
    topics: List[str]
    sentiment: str
    user_preferences: Dict[str, Any]

@dataclass
class LearningPattern:
    """Obrazac učenja"""
    pattern_type: str
    input_pattern: str
    output_pattern: str
    success_rate: float
    usage_count: int
    last_used: datetime
    context: Dict[str, Any]

class MemoryEngine:
    """Napredni Memory Engine za AI inteligenciju"""
    
    def __init__(self, memory_file: str = "ai_memory.pkl", max_memories: int = 10000):
        self.memory_file = memory_file
        self.max_memories = max_memories
        
        # Glavne memorije
        self.memories: Dict[str, Memory] = {}
        self.conversation_memories: Dict[str, ConversationMemory] = {}
        self.learning_patterns: Dict[str, LearningPattern] = {}
        
        # Indeksi za brzo pretraživanje
        self.category_index: Dict[str, List[str]] = defaultdict(list)
        self.tag_index: Dict[str, List[str]] = defaultdict(list)
        self.temporal_index: Dict[str, List[str]] = defaultdict(list)
        
        # Cache za brz pristup
        self.recent_memories: deque = deque(maxlen=100)
        self.frequently_accessed: Dict[str, int] = defaultdict(int)
        
        # Učitaj postojeće memorije
        self._load_memories()
        
        logger.info("🧠 Memory Engine uspešno inicijalizovan!")
    
    def _load_memories(self):
        """Učitava memorije iz fajla"""
        try:
            with open(self.memory_file, 'rb') as f:
                data = pickle.load(f)
                self.memories = data.get('memories', {})
                self.conversation_memories = data.get('conversations', {})
                self.learning_patterns = data.get('patterns', {})
                logger.info(f"✅ Učitano {len(self.memories)} memorija")
        except FileNotFoundError:
            logger.info("📝 Kreiran novi memory fajl")
        except Exception as e:
            logger.error(f"❌ Greška pri učitavanju memorija: {e}")
    
    def _save_memories(self):
        """Čuva memorije u fajl"""
        try:
            data = {
                'memories': self.memories,
                'conversations': self.conversation_memories,
                'patterns': self.learning_patterns
            }
            with open(self.memory_file, 'wb') as f:
                pickle.dump(data, f)
            logger.debug("💾 Memorije sačuvane")
        except Exception as e:
            logger.error(f"❌ Greška pri čuvanju memorija: {e}")
    
    def create_memory(self, content: str, context: Dict[str, Any], category: str = "general", 
                      importance: float = 0.5, tags: List[str] = None) -> str:
        """Kreira novu memoriju"""
        try:
            memory_id = hashlib.md5(f"{content}{datetime.now()}".encode()).hexdigest()
            
            memory = Memory(
                id=memory_id,
                content=content,
                context=context,
                timestamp=datetime.now(),
                importance=importance,
                category=category,
                tags=tags or [],
                access_count=0,
                last_accessed=datetime.now(),
                emotional_tone=self._analyze_emotional_tone(content),
                user_satisfaction=0.5
            )
            
            self.memories[memory_id] = memory
            
            # Ažuriraj indekse
            self._update_indexes(memory)
            
            # Proveri limit memorija
            if len(self.memories) > self.max_memories:
                self._cleanup_old_memories()
            
            self._save_memories()
            logger.info(f"🧠 Nova memorija kreirana: {category} - {content[:50]}...")
            
            return memory_id
            
        except Exception as e:
            logger.error(f"❌ Greška pri kreiranju memorije: {e}")
            return None
    
    def _update_indexes(self, memory: Memory):
        """Ažurira indekse za brzo pretraživanje"""
        # Kategorija indeks
        self.category_index[memory.category].append(memory.id)
        
        # Tag indeks
        for tag in memory.tags:
            self.tag_index[tag].append(memory.id)
        
        # Temporal indeks (po danima)
        day_key = memory.timestamp.strftime("%Y-%m-%d")
        self.temporal_index[day_key].append(memory.id)
    
    def search_memories(self, query: str, category: str = None, tags: List[str] = None, 
                       limit: int = 10) -> List[Memory]:
        """Pretražuje memorije na osnovu upita"""
        try:
            query_lower = query.lower()
            results = []
            
            for memory in self.memories.values():
                score = 0
                
                # Tekstualna sličnost
                if query_lower in memory.content.lower():
                    score += 3
                
                # Kategorija
                if category and memory.category == category:
                    score += 2
                
                # Tagovi
                if tags:
                    for tag in tags:
                        if tag in memory.tags:
                            score += 1
                
                # Važnost
                score += memory.importance
                
                # Frekvencija pristupa
                score += min(memory.access_count * 0.1, 1.0)
                
                if score > 0:
                    results.append((memory, score))
            
            # Sortiraj po skoru
            results.sort(key=lambda x: x[1], reverse=True)
            
            # Vrati top rezultate
            return [memory for memory, score in results[:limit]]
            
        except Exception as e:
            logger.error(f"❌ Greška pri pretraživanju memorija: {e}")
            return []
    
    def get_contextual_memories(self, current_context: Dict[str, Any], limit: int = 5) -> List[Memory]:
        """Dohvata memorije relevantne za trenutni kontekst"""
        try:
            relevant_memories = []
            
            for memory in self.memories.values():
                relevance_score = self._calculate_context_relevance(memory, current_context)
                if relevance_score > 0.3:  # Prag relevantnosti
                    relevant_memories.append((memory, relevance_score))
            
            # Sortiraj po relevantnosti
            relevant_memories.sort(key=lambda x: x[1], reverse=True)
            
            return [memory for memory, score in relevant_memories[:limit]]
            
        except Exception as e:
            logger.error(f"❌ Greška pri dohvatanju kontekstualnih memorija: {e}")
            return []
    
    def _calculate_context_relevance(self, memory: Memory, current_context: Dict[str, Any]) -> float:
        """Računa relevantnost memorije za trenutni kontekst"""
        try:
            relevance = 0.0
            
            # Poredi tagove
            for tag in memory.tags:
                if tag in str(current_context).lower():
                    relevance += 0.2
            
            # Poredi kategorije
            if memory.category in str(current_context).lower():
                relevance += 0.3
            
            # Temporalna relevantnost (novije memorije su relevantnije)
            days_old = (datetime.now() - memory.timestamp).days
            if days_old < 7:
                relevance += 0.2
            elif days_old < 30:
                relevance += 0.1
            
            # Važnost memorije
            relevance += memory.importance * 0.2
            
            return min(relevance, 1.0)
            
        except Exception as e:
            logger.error(f"❌ Greška pri računanju relevantnosti: {e}")
            return 0.0
    
    def learn_from_interaction(self, user_input: str, ai_response: str, user_satisfaction: float, 
                              context: Dict[str, Any]):
        """Uči iz interakcije sa korisnikom"""
        try:
            # Kreiraj memoriju o interakciji
            interaction_content = f"User: {user_input}\nAI: {ai_response}"
            self.create_memory(
                content=interaction_content,
                context=context,
                category="interaction",
                importance=user_satisfaction,
                tags=["interaction", "learning", "user_feedback"]
            )
            
            # Ažuriraj learning pattern
            pattern_key = hashlib.md5(user_input.lower().encode()).hexdigest()
            
            if pattern_key in self.learning_patterns:
                pattern = self.learning_patterns[pattern_key]
                pattern.usage_count += 1
                pattern.success_rate = (pattern.success_rate + user_satisfaction) / 2
                pattern.last_used = datetime.now()
            else:
                new_pattern = LearningPattern(
                    pattern_type="user_interaction",
                    input_pattern=user_input.lower(),
                    output_pattern=ai_response,
                    success_rate=user_satisfaction,
                    usage_count=1,
                    last_used=datetime.now(),
                    context=context
                )
                self.learning_patterns[pattern_key] = new_pattern
            
            # Ažuriraj user preferences
            self._update_user_preferences(context, user_satisfaction)
            
            logger.info(f"🧠 Naučeno iz interakcije: satisfaction={user_satisfaction}")
            
        except Exception as e:
            logger.error(f"❌ Greška pri učenju iz interakcije: {e}")
    
    def _update_user_preferences(self, context: Dict[str, Any], satisfaction: float):
        """Ažurira preferencije korisnika"""
        try:
            # Analiziraj kontekst i ažuriraj preferencije
            for key, value in context.items():
                if isinstance(value, str) and len(value) > 3:
                    # Dodaj u tagove za buduće pretraživanje
                    if satisfaction > 0.7:  # Korisnik je zadovoljan
                        self._add_preference_tag(key, value, positive=True)
                    elif satisfaction < 0.3:  # Korisnik nije zadovoljan
                        self._add_preference_tag(key, value, positive=False)
            
        except Exception as e:
            logger.error(f"❌ Greška pri ažuriranju preferencija: {e}")
    
    def _add_preference_tag(self, key: str, value: str, positive: bool):
        """Dodaje tag preferencije"""
        try:
            tag = f"pref_{key}_{value}"
            if positive:
                tag += "_positive"
            else:
                tag += "_negative"
            
            # Kreiraj memoriju o preferenciji
            self.create_memory(
                content=f"User preference: {key}={value} ({'positive' if positive else 'negative'})",
                context={"preference": True, "key": key, "value": value, "positive": positive},
                category="preference",
                importance=0.8,
                tags=[tag, "preference", "user_learning"]
            )
            
        except Exception as e:
            logger.error(f"❌ Greška pri dodavanju preference tag-a: {e}")
    
    def generate_intelligent_response(self, user_input: str, context: Dict[str, Any]) -> str:
        """Generiše inteligentan odgovor na osnovu memorija"""
        try:
            # Pretraži relevantne memorije
            relevant_memories = self.get_contextual_memories(context, limit=3)
            
            if not relevant_memories:
                return "Izvinjavam se, nemam dovoljno informacija za inteligentan odgovor."
            
            # Analiziraj memorije i generiši odgovor
            response_parts = []
            response_parts.append("🧠 **AI Inteligencija aktivirana:**\n")
            
            for memory in relevant_memories:
                # Dodaj relevantnu informaciju
                if memory.category == "interaction":
                    # Izvuci AI odgovor iz interakcije
                    lines = memory.content.split('\n')
                    if len(lines) > 1:
                        ai_part = lines[1].replace("AI: ", "")
                        response_parts.append(f"💡 **Iz prethodne interakcije:** {ai_part}")
                else:
                    response_parts.append(f"📚 **{memory.category.title()}:** {memory.content}")
                
                # Dodaj tagove ako postoje
                if memory.tags:
                    response_parts.append(f"🏷️ **Tagovi:** {', '.join(memory.tags[:3])}")
                
                response_parts.append("")  # Prazan red
            
            # Dodaj learning insights
            learning_insights = self._get_learning_insights(context)
            if learning_insights:
                response_parts.append("🎓 **AI Učenje:**")
                response_parts.append(learning_insights)
                response_parts.append("")
            
            # Dodaj predložene akcije
            suggested_actions = self._generate_suggested_actions(context, relevant_memories)
            if suggested_actions:
                response_parts.append("🎯 **Predložene akcije:**")
                for action in suggested_actions:
                    response_parts.append(f"• {action}")
                response_parts.append("")
            
            # Dodaj follow-up pitanja
            follow_up = self._generate_follow_up_questions(context, relevant_memories)
            if follow_up:
                response_parts.append("💭 **Follow-up pitanja:**")
                for question in follow_up:
                    response_parts.append(f"• {question}")
            
            return "\n".join(response_parts)
            
        except Exception as e:
            logger.error(f"❌ Greška pri generisanju inteligentnog odgovora: {e}")
            return "Izvinjavam se, došlo je do greške u AI inteligenciji."
    
    def _get_learning_insights(self, context: Dict[str, Any]) -> str:
        """Dohvata insights iz učenja"""
        try:
            insights = []
            
            # Analiziraj learning patterns
            for pattern in self.learning_patterns.values():
                if pattern.success_rate > 0.8 and pattern.usage_count > 2:
                    insights.append(f"✅ {pattern.pattern_type}: visok uspeh ({pattern.success_rate:.2f})")
                elif pattern.success_rate < 0.3 and pattern.usage_count > 1:
                    insights.append(f"⚠️ {pattern.pattern_type}: nizak uspeh ({pattern.success_rate:.2f})")
            
            return "\n".join(insights[:3]) if insights else "Nema novih insights-a"
            
        except Exception as e:
            logger.error(f"❌ Greška pri dohvatanju learning insights: {e}")
            return "Nema insights-a"
    
    def _generate_suggested_actions(self, context: Dict[str, Any], memories: List[Memory]) -> List[str]:
        """Generiše predložene akcije na osnovu memorija"""
        try:
            actions = []
            
            # Analiziraj memorije i generiši akcije
            for memory in memories:
                if memory.category == "interaction" and memory.user_satisfaction > 0.7:
                    actions.append("Ponovi uspešnu strategiju iz prethodne interakcije")
                elif memory.category == "preference" and "positive" in str(memory.tags):
                    actions.append(f"Koristi preferenciju: {memory.content}")
                elif memory.category == "general" and memory.importance > 0.8:
                    actions.append(f"Fokusiraj se na: {memory.content[:50]}...")
            
            return actions[:3] if actions else ["Nema predloženih akcija"]
            
        except Exception as e:
            logger.error(f"❌ Greška pri generisanju predloženih akcija: {e}")
            return ["Nema predloženih akcija"]
    
    def _generate_follow_up_questions(self, context: Dict[str, Any], memories: List[Memory]) -> List[str]:
        """Generiše follow-up pitanja na osnovu memorija"""
        try:
            questions = []
            
            # Analiziraj kontekst i memorije
            if "platform" in str(context).lower():
                questions.append("Da li želite da analiziram specifičnu platformu?")
                questions.append("Kako vam se čini trenutna strategija?")
            
            if "earning" in str(context).lower():
                questions.append("Da li želite da optimizujem zaradu?")
                questions.append("Koje platforme su vam najprofitabilnije?")
            
            if "problem" in str(context).lower():
                questions.append("Da li je problem rešen?")
                questions.append("Da li vam treba dodatna pomoć?")
            
            # Dodaj generalna pitanja
            questions.append("Da li imate još pitanja?")
            questions.append("Kako mogu da poboljšam svoje odgovore?")
            
            return questions[:4] if questions else ["Nema follow-up pitanja"]
            
        except Exception as e:
            logger.error(f"❌ Greška pri generisanju follow-up pitanja: {e}")
            return ["Nema follow-up pitanja"]
    
    def _analyze_emotional_tone(self, text: str) -> str:
        """Analizira emocionalni ton teksta"""
        try:
            text_lower = text.lower()
            
            positive_words = ["odlično", "super", "hvala", "zadovoljan", "uspešno", "dobro", "srećan"]
            negative_words = ["problem", "greška", "loše", "nezadovoljan", "frustriran", "teško", "težak"]
            neutral_words = ["informacija", "pitanje", "odgovor", "sistem", "platforma", "nalog"]
            
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            neutral_count = sum(1 for word in neutral_words if word in text_lower)
            
            if positive_count > negative_count:
                return "positive"
            elif negative_count > positive_count:
                return "negative"
            else:
                return "neutral"
                
        except Exception as e:
            logger.error(f"❌ Greška pri analizi emocionalnog tona: {e}")
            return "neutral"
    
    def _cleanup_old_memories(self):
        """Čisti stare memorije"""
        try:
            # Sortiraj po važnosti i pristupu
            memories_list = list(self.memories.items())
            memories_list.sort(key=lambda x: (x[1].importance, x[1].access_count), reverse=True)
            
            # Zadrži top memorije
            keep_count = int(self.max_memories * 0.8)
            memories_to_remove = memories_list[keep_count:]
            
            for memory_id, memory in memories_to_remove:
                del self.memories[memory_id]
                
                # Ukloni iz indeksa
                if memory.id in self.category_index[memory.category]:
                    self.category_index[memory.category].remove(memory.id)
                for tag in memory.tags:
                    if memory.id in self.tag_index[tag]:
                        self.tag_index[tag].remove(memory.id)
            
            logger.info(f"🧹 Očišćeno {len(memories_to_remove)} starih memorija")
            
        except Exception as e:
            logger.error(f"❌ Greška pri čišćenju memorija: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Vraća statistiku memorija"""
        try:
            total_memories = len(self.memories)
            total_conversations = len(self.conversation_memories)
            total_patterns = len(self.learning_patterns)
            
            # Kategorije
            categories = defaultdict(int)
            for memory in self.memories.values():
                categories[memory.category] += 1
            
            # Tagovi
            tags = defaultdict(int)
            for memory in self.memories.values():
                for tag in memory.tags:
                    tags[tag] += 1
            
            # Top tagovi
            top_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                "total_memories": total_memories,
                "total_conversations": total_conversations,
                "total_patterns": total_patterns,
                "categories": dict(categories),
                "top_tags": top_tags,
                "memory_file_size": f"{len(self.memories) * 0.001:.2f} KB"
            }
            
        except Exception as e:
            logger.error(f"❌ Greška pri dohvatanju statistike: {e}")
            return {"error": str(e)}
    
    def clear_memories(self, category: str = None):
        """Briše memorije (opciono po kategoriji)"""
        try:
            if category:
                # Briši samo određenu kategoriju
                memories_to_remove = [mid for mid, m in self.memories.items() if m.category == category]
                for mid in memories_to_remove:
                    del self.memories[mid]
                logger.info(f"🧹 Obrisane memorije kategorije: {category}")
            else:
                # Briši sve memorije
                self.memories.clear()
                self.conversation_memories.clear()
                self.learning_patterns.clear()
                logger.info("🧹 Sve memorije obrisane")
            
            self._save_memories()
            
        except Exception as e:
            logger.error(f"❌ Greška pri brisanju memorija: {e}")

# Globalna instanca
memory_engine = None

def get_memory_engine() -> MemoryEngine:
    """Vraća globalnu instancu Memory Engine-a"""
    global memory_engine
    if memory_engine is None:
        memory_engine = MemoryEngine()
    return memory_engine
