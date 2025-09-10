#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - NLP Engine
Natural Language Processing za AI Asistent
"""

import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class QuestionType(Enum):
    """Tipovi pitanja koje AI može da prepozna"""
    GREETING = "greeting"
    EARNING = "earning"
    PLATFORMS = "platforms"
    CONTENT = "content"
    CRYPTO = "crypto"
    SOCIAL_MEDIA = "social_media"
    SEO = "seo"
    ANALYTICS = "analytics"
    OPTIMIZATION = "optimization"
    GENERAL = "general"
    COMMAND = "command"
    TECHNICAL = "technical"
    HELP = "help"

class QuestionIntent(Enum):
    """Namere korisnika"""
    INFORMATIONAL = "informational"  # Traži informacije
    INSTRUCTIONAL = "instructional"  # Traži instrukcije
    ANALYTICAL = "analytical"        # Traži analizu
    OPTIMIZATION = "optimization"    # Traži optimizaciju
    COMPARISON = "comparison"        # Traži poređenje
    PREDICTION = "prediction"        # Traži predviđanje

@dataclass
class NLPResult:
    """Rezultat NLP analize"""
    question_type: QuestionType
    intent: QuestionIntent
    confidence: float
    keywords: List[str]
    entities: List[str]
    sentiment: str
    language: str
    context: Dict[str, Any]

class NLPEngine:
    """Napredni NLP engine za AI Asistent"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Ključne reči za različite tipove pitanja
        self.keyword_patterns = {
            QuestionType.GREETING: [
                "zdravo", "hello", "hi", "hey", "ćao", "cao", "pozdrav", "dobro jutro", 
                "dobar dan", "dobro veče", "kako si", "kako ste"
            ],
            QuestionType.EARNING: [
                "kako", "how", "zaraditi", "earn", "zarada", "money", "profit", "zaradu",
                "novac", "cash", "dolar", "euro", "plata", "satnica", "prihod", "income",
                "biznis", "business", "posao", "job", "rad", "work"
            ],
            QuestionType.PLATFORMS: [
                "platforme", "platforms", "platforma", "sajt", "website", "app", "aplikacija",
                "textbroker", "iwriter", "medium", "surveys", "mturk", "clickworker", "appen",
                "lionbridge", "fiverr", "upwork", "freelancer"
            ],
            QuestionType.CONTENT: [
                "sadržaj", "content", "članak", "article", "blog", "video", "tekst", "pisati",
                "write", "copywriting", "seo", "naslov", "title", "opis", "description",
                "kreativnost", "creativity", "storytelling"
            ],
            QuestionType.CRYPTO: [
                "kripto", "crypto", "trgovanje", "trading", "bitcoin", "ethereum", "blockchain",
                "wallet", "exchange", "defi", "staking", "mining", "nft", "token", "coin",
                "altcoin", "stablecoin", "yield farming"
            ],
            QuestionType.SOCIAL_MEDIA: [
                "tiktok", "instagram", "youtube", "viral", "trending", "facebook", "twitter",
                "linkedin", "snapchat", "pinterest", "influencer", "engagement", "reach",
                "followers", "likes", "shares", "comments"
            ],
            QuestionType.SEO: [
                "seo", "marketing", "promocija", "promotion", "traffic", "google", "ranking",
                "ključne reči", "keywords", "backlinks", "meta", "optimizacija", "analytics",
                "semrush", "ahrefs", "moz", "search console"
            ],
            QuestionType.ANALYTICS: [
                "analiza", "analytics", "predviđanje", "prediction", "trend", "statistika",
                "podaci", "izveštaj", "report", "kpi", "metrics", "dashboard", "insights",
                "performance", "roi", "conversion", "click rate"
            ],
            QuestionType.OPTIMIZATION: [
                "optimizacija", "optimization", "poboljšanje", "improvement", "bolje", "efikasnost",
                "efficiency", "automation", "workflow", "process", "strategy", "taktika",
                "plan", "approach", "methodology"
            ],
            QuestionType.COMMAND: [
                "pokreni", "start", "zaustavi", "stop", "dodaj", "add", "kreiraj", "create",
                "otvori", "open", "prikaži", "show", "analiziraj", "analyze", "izvrši", "execute"
            ],
            QuestionType.TECHNICAL: [
                "problem", "greška", "error", "bug", "ne radi", "doesn't work", "crash",
                "slow", "spor", "freeze", "zamrzava", "restart", "restartuj", "update",
                "ažuriraj", "install", "instaliraj"
            ],
            QuestionType.HELP: [
                "pomoć", "help", "savet", "advice", "kako", "how", "šta", "sta", "what",
                "ko", "who", "gde", "where", "kada", "when", "zašto", "zasto", "why"
            ]
        }
        
        # Sentiment analiza
        self.sentiment_patterns = {
            "positive": ["odlično", "super", "fantastično", "sjajno", "briljantno", "genijalno"],
            "negative": ["loše", "užasno", "katastrofa", "problem", "greška", "ne radi"],
            "neutral": ["ok", "u redu", "normalno", "standardno", "obično"]
        }
        
        # Jezici
        self.language_patterns = {
            "sr": ["kako", "šta", "ko", "gde", "kada", "zašto", "zdravo", "hvala"],
            "en": ["how", "what", "who", "where", "when", "why", "hello", "thanks"],
            "mixed": ["kako", "how", "šta", "what", "zdravo", "hello"]
        }
        
        self.logger.info("🧠 NLP Engine uspešno inicijalizovan")
    
    def analyze_text(self, text: str) -> NLPResult:
        """Glavna metoda za analizu teksta"""
        try:
            text_lower = text.lower().strip()
            
            # Osnovna analiza
            question_type = self._classify_question_type(text_lower)
            intent = self._determine_intent(text_lower)
            confidence = self._calculate_confidence(text_lower, question_type)
            keywords = self._extract_keywords(text_lower)
            entities = self._extract_entities(text_lower)
            sentiment = self._analyze_sentiment(text_lower)
            language = self._detect_language(text_lower)
            context = self._extract_context(text_lower)
            
            result = NLPResult(
                question_type=question_type,
                intent=intent,
                confidence=confidence,
                keywords=keywords,
                entities=entities,
                sentiment=sentiment,
                language=language,
                context=context
            )
            
            self.logger.info(f"NLP Analiza: '{text}' → {question_type.value} (confidence: {confidence:.2f})")
            return result
            
        except Exception as e:
            self.logger.error(f"Greška u NLP analizi: {e}")
            # Fallback rezultat
            return NLPResult(
                question_type=QuestionType.GENERAL,
                intent=QuestionIntent.INFORMATIONAL,
                confidence=0.5,
                keywords=[],
                entities=[],
                sentiment="neutral",
                language="unknown",
                context={}
            )
    
    def _classify_question_type(self, text: str) -> QuestionType:
        """Klasifikuje tip pitanja"""
        try:
            # Brojimo ključne reči za svaki tip
            type_scores = {}
            
            for question_type, keywords in self.keyword_patterns.items():
                score = sum(1 for keyword in keywords if keyword in text)
                if score > 0:
                    type_scores[question_type] = score
            
            if not type_scores:
                return QuestionType.GENERAL
            
            # Vraćamo tip sa najviše ključnih reči
            best_type = max(type_scores.items(), key=lambda x: x[1])[0]
            
            # Posebna pravila za precizniju klasifikaciju
            if "zdravo" in text or "hello" in text or "hi" in text:
                return QuestionType.GREETING
            
            if any(word in text for word in ["kako", "how", "zašto", "why"]):
                if best_type == QuestionType.EARNING:
                    return QuestionType.EARNING
                elif best_type == QuestionType.PLATFORMS:
                    return QuestionType.PLATFORMS
            
            return best_type
            
        except Exception as e:
            self.logger.error(f"Greška u klasifikaciji tipa pitanja: {e}")
            return QuestionType.GENERAL
    
    def _determine_intent(self, text: str) -> QuestionIntent:
        """Određuje nameru korisnika"""
        try:
            # Pitanja sa "kako", "zašto" su obično informativna
            if any(word in text for word in ["kako", "how", "zašto", "why", "šta", "what"]):
                return QuestionIntent.INFORMATIONAL
            
            # Pitanja sa "koji", "koje" su poređenja
            if any(word in text for word in ["koji", "koje", "which", "ko", "who"]):
                return QuestionIntent.COMPARISON
            
            # Pitanja sa "kada", "gde" su analitička
            if any(word in text for word in ["kada", "when", "gde", "where"]):
                return QuestionIntent.ANALYTICAL
            
            # Komande su instrukcijske
            if any(word in text for word in ["pokreni", "start", "zaustavi", "stop", "dodaj", "add"]):
                return QuestionIntent.INSTRUCTIONAL
            
            # Optimizacija
            if any(word in text for word in ["optimizuj", "optimize", "poboljšaj", "improve"]):
                return QuestionIntent.OPTIMIZATION
            
            # Predviđanje
            if any(word in text for word in ["predviđaj", "predict", "trend", "budućnost", "future"]):
                return QuestionIntent.PREDICTION
            
            return QuestionIntent.INFORMATIONAL
            
        except Exception as e:
            self.logger.error(f"Greška u određivanju namere: {e}")
            return QuestionIntent.INFORMATIONAL
    
    def _calculate_confidence(self, text: str, question_type: QuestionType) -> float:
        """Računa pouzdanost klasifikacije"""
        try:
            keywords = self.keyword_patterns.get(question_type, [])
            if not keywords:
                return 0.5
            
            # Brojimo koliko ključnih reči je pronađeno
            found_keywords = sum(1 for keyword in keywords if keyword in text)
            total_keywords = len(keywords)
            
            # Osnovna pouzdanost
            base_confidence = found_keywords / total_keywords if total_keywords > 0 else 0
            
            # Bonus za duže tekstove
            length_bonus = min(len(text.split()) / 10, 0.2)
            
            # Bonus za specifične reči
            specificity_bonus = 0.1 if any(word in text for word in ["ai", "artificial", "intelligence"]) else 0
            
            confidence = min(base_confidence + length_bonus + specificity_bonus, 1.0)
            return round(confidence, 2)
            
        except Exception as e:
            self.logger.error(f"Greška u računanju pouzdanosti: {e}")
            return 0.5
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Izvlači ključne reči iz teksta"""
        try:
            keywords = []
            
            # Dodajemo sve ključne reči koje su pronađene
            for question_type, patterns in self.keyword_patterns.items():
                for pattern in patterns:
                    if pattern in text:
                        keywords.append(pattern)
            
            # Dodajemo specifične reči
            specific_words = ["ai", "artificial", "intelligence", "zarada", "profit", "platforma", "content"]
            for word in specific_words:
                if word in text:
                    keywords.append(word)
            
            return list(set(keywords))  # Uklanjamo duplikate
            
        except Exception as e:
            self.logger.error(f"Greška u izvlačenju ključnih reči: {e}")
            return []
    
    def _extract_entities(self, text: str) -> List[str]:
        """Izvlači entitete (platforme, valute, itd.)"""
        try:
            entities = []
            
            # Platforme
            platforms = ["textbroker", "iwriter", "medium", "fiverr", "upwork", "freelancer"]
            for platform in platforms:
                if platform in text:
                    entities.append(f"platform:{platform}")
            
            # Valute
            currencies = ["dolar", "dollar", "euro", "rsd", "din", "usd", "eur"]
            for currency in currencies:
                if currency in text:
                    entities.append(f"currency:{currency}")
            
            # Kriptovalute
            crypto = ["bitcoin", "ethereum", "btc", "eth", "ada", "sol", "matic"]
            for coin in crypto:
                if coin in text:
                    entities.append(f"crypto:{coin}")
            
            return entities
            
        except Exception as e:
            self.logger.error(f"Greška u izvlačenju entiteta: {e}")
            return []
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analizira sentiment teksta"""
        try:
            positive_count = sum(1 for word in self.sentiment_patterns["positive"] if word in text)
            negative_count = sum(1 for word in self.sentiment_patterns["negative"] if word in text)
            neutral_count = sum(1 for word in self.sentiment_patterns["neutral"] if word in text)
            
            if positive_count > negative_count and positive_count > neutral_count:
                return "positive"
            elif negative_count > positive_count and negative_count > neutral_count:
                return "negative"
            else:
                return "neutral"
                
        except Exception as e:
            self.logger.error(f"Greška u sentiment analizi: {e}")
            return "neutral"
    
    def _detect_language(self, text: str) -> str:
        """Detektuje jezik teksta"""
        try:
            sr_count = sum(1 for word in self.language_patterns["sr"] if word in text)
            en_count = sum(1 for word in self.language_patterns["en"] if word in text)
            
            if sr_count > en_count:
                return "sr"
            elif en_count > sr_count:
                return "en"
            else:
                return "mixed"
                
        except Exception as e:
            self.logger.error(f"Greška u detekciji jezika: {e}")
            return "unknown"
    
    def _extract_context(self, text: str) -> Dict[str, Any]:
        """Izvlači kontekst iz teksta"""
        try:
            context = {
                "is_question": any(word in text for word in ["?", "kako", "how", "šta", "what"]),
                "is_command": any(word in text for word in ["pokreni", "start", "zaustavi", "stop"]),
                "is_urgent": any(word in text for word in ["hitno", "urgent", "sada", "now", "odmah", "immediately"]),
                "is_complex": len(text.split()) > 10,
                "has_numbers": bool(re.search(r'\d+', text)),
                "has_emojis": bool(re.search(r'[^\w\s]', text))
            }
            
            return context
            
        except Exception as e:
            self.logger.error(f"Greška u izvlačenju konteksta: {e}")
            return {}

# Globalna instanca NLP Engine-a
nlp_engine = NLPEngine()

def get_nlp_engine() -> NLPEngine:
    """Vraća globalnu instancu NLP Engine-a"""
    return nlp_engine

def analyze_text(text: str) -> NLPResult:
    """Brza funkcija za analizu teksta"""
    return nlp_engine.analyze_text(text)
