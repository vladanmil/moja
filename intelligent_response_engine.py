#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - Intelligent Response Engine
Generiše inteligentne odgovore na osnovu NLP analize
"""

import logging
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from .nlp_engine import NLPResult, QuestionType, QuestionIntent

logger = logging.getLogger(__name__)

class IntelligentResponseEngine:
    """Engine za generisanje inteligentnih AI odgovora"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.response_templates = {}
        self.conversation_history = []
        self.user_preferences = {}
        
        # Učitavanje response template-a
        self._load_response_templates()
        
        self.logger.info("🧠 Intelligent Response Engine uspešno inicijalizovan")
    
    def _load_response_templates(self):
        """Učitava template-e za odgovore"""
        self.response_templates = {
            QuestionType.GREETING: {
                "templates": [
                    """👋 **AI Asistent - Pametni Pozdrav:**

Zdravo! Drago mi je što ste ovde! 🎉

**🚀 Šta mogu da uradim za vas:**

**💰 Zarada i strategije:**
• Analiziram platforme za maksimalnu zaradu
• Predlažem AI-optimizovane strategije
• Optimizujem vaše radne procese

**🎯 Specifična pitanja:**
• "Kako da zaradim više?" → AI strategije zarade
• "Koje su najbolje platforme?" → Platform analiza
• "Kako da napravim viral sadržaj?" → Content AI
• "AI analiza zarade" → Prediktivna analiza

**🤖 AI funkcionalnosti:**
• Earning AI - strategije zarade
• Content AI - generisanje sadržaja
• Crypto AI - trgovanje i DeFi
• Social Media AI - viral strategije
• SEO AI - Google optimizacija
• Analytics AI - predviđanje trendova

**💡 Preporučujem:**
Pitajte me bilo šta o zaradi, platformama ili strategijama!
Ja sam ovde da vam pomognem da maksimalizujete vašu zaradu! 💪

Kako vam mogu pomoći danas?""",
                    
                    """🎉 **AI Asistent - Pozdrav i Dobrodošlica:**

Ćao! Dobrodošli u AutoEarnPro 2.0! 🚀

**🎯 Moje AI sposobnosti:**
• **Earning AI** - strategije za maksimalnu zaradu
• **Content AI** - viral sadržaj i blog strategije
• **Crypto AI** - trading i DeFi prilike
• **Social Media AI** - TikTok, Instagram, YouTube
• **SEO AI** - Google ranking i traffic
• **Analytics AI** - predviđanje trendova

**💬 Primeri pitanja:**
• "Kako da zaradim više na platformama?"
• "AI analiza najboljih platformi"
• "Kako da napravim viral TikTok sadržaj?"
• "AI strategija za crypto trading"

**🚀 Preporučujem:**
Pitajte me bilo šta - ja sam ovde da pomognem!
Kako vam mogu pomoći danas?"""
                ],
                "fallback": "Zdravo! Kako vam mogu pomoći danas?"
            },
            
            QuestionType.EARNING: {
                "templates": [
                    """🎯 **AI Analiza: Kako da zaradite VIŠE:**

🚀 **Napredne AI strategije za maksimalnu zaradu:**

1. **AI-Optimizovana Diversifikacija:**
   • Koristite 10-15 platformi istovremeno
   • AI automatski balansira aktivnost
   • Fokus na platforme sa najboljim ROI

2. **Inteligentno Upravljanje Vremenom:**
   • AI analizira najprofitabilnije časove
   • Automatska optimizacija radnih procesa
   • Predviđanje trendova i prilika

3. **AI-Enhanced Reputacija:**
   • Automatsko praćenje kvaliteta rada
   • Predviđanje potreba za radnicima
   • Strategijsko planiranje karijere

4. **Napredne AI Automatizacije:**
   • Automatsko pokretanje platformi
   • Inteligentno balansiranje zadataka
   • Prediktivna analiza tržišta

5. **AI-Driven Analytics:**
   • Real-time analiza performansi
   • Predviđanje zarade na 30-90 dana
   • Optimizacija na osnovu podataka

💡 **AI Preporučujem:** Koristite 'Auto Mode' + 'AI Optimization' za maksimalnu zaradu!""",
                    
                    """💰 **AI Strategije za Zaradu:**

🎯 **Earning Obsessed AI je aktivan i analizira:**

• **Platforme:** Automatska optimizacija aktivnosti
• **Vreme:** Inteligentno planiranje rada  
• **Strategije:** AI-generisane taktike zarade
• **Analitika:** Prediktivna analiza tržišta
• **Automatizacija:** Smart workflow optimizacija

**🏆 Najbolje platforme za zaradu:**
• Textbroker: $15-50 po članku
• iWriter: $10-40 po članku
• Medium: $100-500 po članku
• Amazon MTurk: $0.50-20 po zadatku
• Lionbridge: $15-50 po satu

**💡 Preporučujem:**
• Koristite 'Auto Mode' za automatsko pokretanje
• Diversifikujte na 5-10 platformi
• Fokusirajte se na content writing
• Gradite reputaciju za veće plate

Kako vam mogu konkretno pomoći sa zaradom?"""
                ],
                "fallback": "Earning AI je ovde da vam pomogne sa strategijama zarade!"
            },
            
            QuestionType.PLATFORMS: {
                "templates": [
                    """🏆 **AI Platform Optimization:**

🚀 **Ultra Optimization Engine je aktivan:**

**Content Writing (Najbolje plate):**
• Textbroker - $15-50 po članku (AI-optimizovano)
• iWriter - $10-40 po članku (Smart matching)
• Medium - $100-500 po članku (Viral prediction)

**Surveys (Stabilan prihod):**
• Survey Junkie - $1-5 po anketi (AI filtering)
• Swagbucks - $0.50-3 po anketi (Smart selection)
• Pinecone Research - $3-5 po anketi (Quality focus)

**Microtasks (Brzi novac):**
• Amazon MTurk - $0.50-20 po zadatku (AI sorting)
• Clickworker - $0.10-5 po zadatku (Smart routing)
• Appen - $5-50 po projektu (AI matching)

**Data Annotation (Visoke plate):**
• Lionbridge - $15-50 po satu (AI optimization)
• TELUS International - $12-40 po satu (Smart workflow)

💡 **AI Strategija:** Koristite 'Auto Mode' + 'Smart Optimization' za maksimalnu zaradu!""",
                    
                    """📱 **AI Platform Analiza:**

🎯 **Platform Monitor Assistant je aktivan:**

**Top 5 Platformi za Zaradu:**
1. **Textbroker** - Content writing, $15-50/članak
2. **iWriter** - Copywriting, $10-40/članak
3. **Medium** - Blog monetization, $100-500/članak
4. **Amazon MTurk** - Microtasks, $0.50-20/zadatak
5. **Lionbridge** - Data annotation, $15-50/sat

**AI Optimizacija:**
• Automatsko balansiranje aktivnosti
• Smart task selection
• Performance tracking
• ROI optimization

**💡 Preporučujem:**
• Fokusirajte se na content writing platforme
• Koristite AI-optimizovane strategije
• Gradite reputaciju za veće plate
• Diversifikujte na više platformi

Koju platformu želite da detaljno analiziram?"""
                ],
                "fallback": "AI Platform analiza je dostupna za sve platforme!"
            },
            
            QuestionType.CONTENT: {
                "templates": [
                    """🎨 **AI Content Generation:**

🚀 **Content Generator AI je aktivan:**

**Blog Strategije:**
• AI-generisani naslovi koji privlače klikove
• SEO-optimizovani članci za Google
• Viral content predviđanje
• Trend analiza za maksimalan engagement

**Video Sadržaj:**
• TikTok viral strategije
• YouTube optimization
• Instagram Reels taktike
• Cross-platform content distribution

**Content Monetization:**
• Affiliate link optimization
• Ad placement strategies
• Sponsored content matching
• Revenue maximization

💡 **AI Preporučujem:** Koristite 'Content Generator' + 'SEO Optimizer' za maksimalan reach!""",
                    
                    """📝 **AI Content Strategije:**

🎯 **Content AI je spreman za pomoć:**

**Viral Content Formula:**
• **Hook:** Prvi 3 sekundi su ključni
• **Story:** Emotivna priča = više shares
• **Trending:** Koristite aktuelne hashtag-ove
• **Timing:** Post u najbolje vreme (7-9 PM)

**Platform-Specific Strategije:**
• **TikTok:** Kratki, energični videoi (15-60s)
• **Instagram:** Visokokvalitetne slike + Stories
• **YouTube:** SEO-optimizovani naslovi + thumbnails
• **Blog:** Long-form sadržaj (2000+ reči)

**AI Tools:**
• Content Generator - automatski sadržaj
• SEO Optimizer - Google ranking
• Viral Predictor - trend analiza
• Engagement Analyzer - performance tracking

**💡 Preporučujem:**
• Fokusirajte se na jednu platformu
• Kreirajte konzistentan sadržaj
• Koristite AI za optimizaciju
• Pratite performanse

Kakav sadržaj želite da kreiramo?"""
                ],
                "fallback": "Content AI je ovde da vam pomogne sa sadržajem!"
            },
            
            QuestionType.CRYPTO: {
                "templates": [
                    """₿ **AI Crypto & Trading:**

🚀 **Crypto Earning Engine je aktivan:**

**Trading Strategije:**
• AI-predviđanje tržišnih trendova
• Automatska arbitraža između exchange-ova
• Smart portfolio management
• Risk assessment i optimization

**DeFi Opportunities:**
• Yield farming optimization
• Liquidity mining strategies
• Staking optimization
• Flash loan arbitrage

**Market Intelligence:**
• Real-time price monitoring
• News sentiment analysis
• Whale wallet tracking
• Market manipulation detection

💡 **AI Preporučujem:** Koristite 'Crypto Engine' + 'Market Intelligence' za maksimalnu zaradu!""",
                    
                    """🚀 **AI Crypto Strategije:**

🎯 **Crypto AI analizira tržište:**

**Top Kriptovalute za Zaradu:**
• **Bitcoin (BTC):** Store of value, long-term
• **Ethereum (ETH):** DeFi platform, staking
• **Cardano (ADA):** Proof of stake, low fees
• **Solana (SOL):** Fast transactions, DeFi
• **Polygon (MATIC):** Layer 2 scaling

**DeFi Strategije:**
• **Yield Farming:** 20-100% APY
• **Liquidity Provision:** Trading fee revenue
• **Staking:** 5-15% APY
• **Arbitrage:** Price differences između exchange-ova

**AI Tools:**
• Market Predictor - trend analiza
• Risk Manager - portfolio protection
• Yield Optimizer - DeFi strategies
• Arbitrage Bot - automatska zarada

**💡 Preporučujem:**
• Počnite sa BTC/ETH
• Diversifikujte portfolio
• Koristite AI za analizu
• Pratite risk management

Koju crypto strategiju želite da analiziramo?"""
                ],
                "fallback": "Crypto AI je ovde za trading strategije!"
            },
            
            QuestionType.SOCIAL_MEDIA: {
                "templates": [
                    """📱 **AI Social Media:**

🚀 **TikTok Viral Engine je aktivan:**

**Viral Strategije:**
• AI-predviđanje trending hashtag-ova
• Optimal timing za postove
• Content virality prediction
• Audience engagement optimization

**Cross-Platform:**
• Instagram Reels optimization
• YouTube Shorts strategies
• Twitter viral tactics
• LinkedIn professional content

**Monetization:**
• Influencer collaboration matching
• Brand partnership optimization
• Affiliate marketing automation
• Revenue stream diversification

💡 **AI Preporučujem:** Koristite 'TikTok Engine' + 'Viral Prediction' za maksimalan reach!""",
                    
                    """🎬 **AI Social Media Mastery:**

🎯 **Social Media AI je spreman:**

**Viral Content Formula:**
• **Hook:** Prvi 3 sekundi su ključni
• **Trending:** Koristite aktuelne hashtag-ove
• **Emotion:** Emotivni sadržaj = više shares
• **Timing:** Post u najbolje vreme

**Platform-Specific:**
• **TikTok:** 15-60s videoi, trending sounds
• **Instagram:** Reels + Stories + Posts
• **YouTube:** Shorts + Long-form content
• **Twitter:** Threads + viral tweets

**AI Optimization:**
• Hashtag Predictor - trending tags
• Timing Optimizer - best posting times
• Content Analyzer - performance tracking
• Audience Insights - engagement metrics

**💡 Preporučujem:**
• Fokusirajte se na 2-3 platforme
• Kreirajte konzistentan sadržaj
• Koristite AI za optimizaciju
• Pratite viral trends

Koju platformu želite da optimizujemo?"""
                ],
                "fallback": "Social Media AI je ovde za viral strategije!"
            },
            
            QuestionType.SEO: {
                "templates": [
                    """🔍 **AI SEO Optimization:**

🚀 **SEO Optimizer AI je aktivan:**

**Keyword Research:**
• AI-predviđanje trending keywords
• Long-tail keyword optimization
• Competitor analysis automation
• Search intent optimization

**Content Optimization:**
• AI-generated meta descriptions
• Smart internal linking
• Schema markup optimization
• Core Web Vitals improvement

**Ranking Strategies:**
• Backlink opportunity detection
• Technical SEO automation
• Local SEO optimization
• E-commerce SEO tactics

💡 **AI Preporučujem:** Koristite 'SEO Optimizer' + 'Content Generator' za maksimalan traffic!""",
                    
                    """📈 **AI SEO Mastery:**

🎯 **SEO AI optimizuje vaš ranking:**

**Keyword Research:**
• **Primary Keywords:** Glavne ključne reči
• **Long-tail:** Specifične fraze (manja konkurencija)
• **LSI Keywords:** Semantički povezane reči
• **Trending:** Aktuelni search terms

**On-Page Optimization:**
• **Title Tags:** 50-60 karaktera, keyword na početku
• **Meta Descriptions:** 150-160 karaktera, call-to-action
• **Header Tags:** H1, H2, H3 hijerarhija
• **Content:** 2000+ reči, keyword density 1-2%

**Technical SEO:**
• **Page Speed:** Core Web Vitals optimization
• **Mobile-First:** Responsive design
• **Schema Markup:** Rich snippets
• **Internal Linking:** Site architecture

**💡 Preporučujem:**
• Fokusirajte se na long-tail keywords
• Optimizujte page speed
• Kreirajte kvalitetan sadržaj
• Koristite AI za analizu

Koju SEO strategiju želite da implementiramo?"""
                ],
                "fallback": "SEO AI je ovde za Google optimizaciju!"
            },
            
            QuestionType.ANALYTICS: {
                "templates": [
                    """📊 **AI Predictive Analytics:**

🚀 **Predictive Analytics Suite je aktivan:**

**Market Predictions:**
• AI-predviđanje tržišnih trendova
• Platform performance forecasting
• Revenue prediction models
• Risk assessment automation

**Performance Analytics:**
• Real-time KPI monitoring
• Automated reporting
• Trend analysis
• Optimization recommendations

**Business Intelligence:**
• Competitive analysis
• Market opportunity detection
• ROI optimization
• Strategic planning support

💡 **AI Preporučujem:** Koristite 'Analytics Suite' + 'Market Intelligence' za data-driven odluke!""",
                    
                    """📊 **AI Analytics Mastery:**

🎯 **Analytics AI analizira performanse:**

**Key Metrics (KPI):**
• **Traffic:** Page views, unique visitors
• **Engagement:** Time on page, bounce rate
• **Conversion:** Click-through rate, sales
• **Revenue:** Earnings per platform, ROI

**Trend Analysis:**
• **Daily Trends:** Kratkoročne promene
• **Weekly Patterns:** Ciklične varijacije
• **Monthly Growth:** Dugoročni trendovi
• **Seasonal Effects:** Godišnje varijacije

**AI Predictions:**
• **Revenue Forecasting:** 30-90 dana unapred
• **Platform Performance:** Predviđanje uspeha
• **Market Trends:** Tržišne prognoze
• **Risk Assessment:** Identifikacija rizika

**💡 Preporučujem:**
• Pratite KPI-e redovno
• Analizirajte trendove
• Koristite AI predviđanja
• Optimizujte na osnovu podataka

Koju analizu želite da pokrenemo?"""
                ],
                "fallback": "Analytics AI je ovde za predviđanja!"
            },
            
            QuestionType.OPTIMIZATION: {
                "templates": [
                    """⚡ **AI Ultra Optimization:**

🚀 **Ultra Optimization Engine je aktivan:**

**Workflow Optimization:**
• AI-automated task scheduling
• Smart resource allocation
• Performance bottleneck detection
• Efficiency maximization

**Process Automation:**
• Intelligent workflow design
• Automated decision making
• Predictive maintenance
• Quality assurance automation

**System Optimization:**
• Performance tuning
• Resource optimization
• Scalability planning
• Cost reduction strategies

💡 **AI Preporučujem:** Koristite 'Optimization Engine' + 'Smart Automation' za maksimalnu efikasnost!""",
                    
                    """🚀 **AI Optimization Mastery:**

🎯 **Optimization AI maksimizuje efikasnost:**

**Workflow Optimization:**
• **Task Scheduling:** AI-optimizovano planiranje
• **Resource Allocation:** Pametna raspodela resursa
• **Bottleneck Detection:** Identifikacija uskih grla
• **Efficiency Metrics:** Performance tracking

**Process Automation:**
• **Workflow Design:** Inteligentni procesi
• **Decision Making:** Automatske odluke
• **Quality Control:** Kontinualna provera
• **Performance Monitoring:** Real-time tracking

**System Optimization:**
• **Performance Tuning:** Maksimalna brzina
• **Resource Management:** Optimalno korišćenje
• **Scalability:** Rast bez gubitka performansi
• **Cost Reduction:** Maksimalna efikasnost

**💡 Preporučujem:**
• Automatizujte repetitivne zadatke
• Optimizujte workflow-ove
• Pratite performance metrike
• Koristite AI za optimizaciju

Koju optimizaciju želite da implementiramo?"""
                ],
                "fallback": "Optimization AI je ovde za maksimalnu efikasnost!"
            },
            
            QuestionType.GENERAL: {
                "templates": [
                    """🤔 **AI Asistent - Inteligentna Analiza:**

'{message}' je odlično pitanje! 🧠

**💭 Moja AI analiza:**
• Razumem šta tražite
• Imam pristup celom sistemu
• Mogu da izvršim akcije u vaše ime
• Koristim napredne AI module za odgovore

**🎯 Šta mogu da uradim:**
• **Zarada:** Strategije, platforme, optimizacija
• **Content:** Blog, video, viral sadržaj
• **Crypto:** Trading, DeFi, analiza tržišta
• **Social Media:** TikTok, Instagram, YouTube
• **SEO:** Google optimizacija, marketing
• **Analytics:** Predviđanje, trendovi, KPI

**🚀 AI funkcionalnosti:**
• Earning Obsessed AI - maksimalna zarada
• Content Generator AI - viral sadržaj
• Crypto Earning Engine - kripto strategije
• TikTok Viral Engine - viral marketing
• SEO Optimizer AI - Google ranking
• Predictive Analytics - tržišne prognoze

**💡 Preporučujem:**
• Pitajte konkretno: "Kako da zaradim više?"
• Koristite komande: "status", "analiza", "pokreni sve"
• Tražite AI savete: "AI strategija za [platforma]"

**Kako vam mogu konkretno pomoći sa '{message}'?""",
                    
                    """🧠 **AI Asistent - Pametna Podrška:**

'{message}' je interesantno pitanje! 💡

**🎯 Moje AI sposobnosti:**
• **Earning AI:** Strategije za maksimalnu zaradu
• **Content AI:** Viral sadržaj i blog strategije
• **Crypto AI:** Trading i DeFi prilike
• **Social Media AI:** TikTok, Instagram, YouTube
• **SEO AI:** Google ranking i traffic
• **Analytics AI:** Predviđanje trendova

**💬 Primeri pitanja:**
• "Kako da zaradim više na platformama?"
• "AI analiza najboljih platformi"
• "Kako da napravim viral TikTok sadržaj?"
• "AI strategija za crypto trading"

**🚀 Preporučujem:**
• Pitajte konkretno šta želite
• Koristite AI funkcionalnosti
• Tražite strategije i savete
• Koristite komande sistema

**Kako vam mogu pomoći sa '{message}'?"""
                ],
                "fallback": "AI Asistent je ovde da vam pomogne!"
            },
            
            QuestionType.COMMAND: {
                "templates": [
                    """⚡ **AI Asistent - Komande:**

'{message}' je komanda! 🚀

**🎯 Dostupne komande:**
• **Platforme:** "pokreni sve", "zaustavi sve", "auto mode"
• **Nalozi:** "dodaj nalog", "dodaj email", "master nalog"
• **Analiza:** "analiza", "status", "limiti", "isplate"
• **AI:** "AI analiza zarade", "AI strategija platformi"

**🤖 AI funkcionalnosti:**
• Earning AI - strategije zarade
• Content AI - generisanje sadržaja
• Crypto AI - trgovanje i DeFi
• Social Media AI - viral strategije
• SEO AI - Google optimizacija
• Analytics AI - predviđanje trendova

**💡 Preporučujem:**
• Koristite komande za brze akcije
• Tražite AI savete za strategije
• Analizirajte performanse redovno
• Optimizujte sa AI pomoći

**Koju komandu želite da izvršim?"""
                ],
                "fallback": "AI Asistent je ovde za komande!"
            },
            
            QuestionType.TECHNICAL: {
                "templates": [
                    """🔧 **AI Asistent - Tehnička Podrška:**

'{message}' je tehnički problem! 🛠️

**🔍 Dijagnostika problema:**
• **Status sistema:** Proverite sa komandom "status"
• **Log fajlovi:** Proverite 'logs' direktorijum
• **Restart:** Zatvorite i ponovo otvorite program
• **AI analiza:** Koristite "AI analiza problema"

**🚀 Rešenja:**
• **Platforme se ne pokreću:** Koristite "pokreni sve"
• **GUI se ne učitava:** Restart programa
• **AI Asistent ne radi:** Proverite konfiguraciju
• **Greške:** Proverite log fajlove

**💡 Preporučujem:**
• Prvo proverite status sistema
• Koristite AI analizu za dijagnostiku
• Proverite log fajlove za detalje
• Restartujte sistem ako je potrebno

**Kako vam mogu pomoći sa problemom?"""
                ],
                "fallback": "AI Asistent je ovde za tehničku podršku!"
            },
            
            QuestionType.HELP: {
                "templates": [
                    """🤖 **AI Asistent - Pomoć i Podrška:**

'{message}' je pitanje za pomoć! 💪

**🎯 Kako vam mogu pomoći:**

**💰 Zarada i strategije:**
• AI strategije za maksimalnu zaradu
• Platforme i optimizacija
• Content i marketing strategije
• Crypto i trading prilike

**🚀 AI funkcionalnosti:**
• Earning AI - strategije zarade
• Content AI - generisanje sadržaja
• Crypto AI - trgovanje i DeFi
• Social Media AI - viral strategije
• SEO AI - Google optimizacija
• Analytics AI - predviđanje trendova

**💬 Primeri pitanja:**
• "Kako da zaradim više na platformama?"
• "AI analiza najboljih platformi"
• "Kako da napravim viral sadržaj?"
• "AI strategija za crypto trading"

**⚡ Komande sistema:**
• "pokreni sve" - Pokreće sve platforme
• "status" - Prikazuje stanje sistema
• "analiza" - Pokreće analizu
• "dodaj email" - Kreira email nalog

**💡 Preporučujem:**
• Pitajte konkretno šta želite
• Koristite AI funkcionalnosti
• Tražite strategije i savete
• Koristite komande sistema

**Kako vam mogu konkretno pomoći?"""
                ],
                "fallback": "AI Asistent je ovde da vam pomogne!"
            }
        }
    
    def generate_response(self, nlp_result: NLPResult, user_message: str = "") -> str:
        """Generiše inteligentan odgovor na osnovu NLP analize"""
        try:
            question_type = nlp_result.question_type
            confidence = nlp_result.confidence
            
            # Logging
            self.logger.info(f"Generisanje odgovora za tip: {question_type.value}, confidence: {confidence}")
            
            # Dodajemo u istoriju
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'user_message': user_message,
                'nlp_result': nlp_result,
                'response_type': question_type.value
            })
            
            # Generisanje odgovora
            if question_type in self.response_templates:
                templates = self.response_templates[question_type]["templates"]
                fallback = self.response_templates[question_type]["fallback"]
                
                # Ako je confidence visok, koristimo detaljniji template
                if confidence > 0.7 and templates:
                    # Personalizujemo odgovor
                    response = self._personalize_response(random.choice(templates), user_message, nlp_result)
                else:
                    # Koristimo fallback
                    response = self._personalize_response(fallback, user_message, nlp_result)
            else:
                # Default odgovor
                response = self._generate_default_response(user_message, nlp_result)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Greška u generisanju odgovora: {e}")
            return f"🤖 **AI Asistent:** Izvinjavam se, imam tehnički problem. Pokušajte ponovo ili koristite 'status' komandu."
    
    def _personalize_response(self, template: str, user_message: str, nlp_result: NLPResult) -> str:
        """Personalizuje odgovor na osnovu korisnika i konteksta"""
        try:
            # Zamena placeholder-a
            response = template.replace("{message}", user_message)
            
            # Dodavanje personalizacije na osnovu sentiment-a
            if nlp_result.sentiment == "positive":
                response += "\n\n😊 **AI Asistent:** Vidim da ste pozitivno raspoloženi! To je odlično za zaradu!"
            elif nlp_result.sentiment == "negative":
                response += "\n\n🤗 **AI Asistent:** Ne brinite, zajedno ćemo rešiti sve probleme!"
            
            # Dodavanje na osnovu jezika
            if nlp_result.language == "sr":
                response += "\n\n🇷🇸 **AI Asistent:** Komuniciramo na srpskom - to je odlično!"
            elif nlp_result.language == "en":
                response += "\n\n🇺🇸 **AI Asistent:** We're communicating in English - that's great!"
            
            # Dodavanje na osnovu confidence
            if nlp_result.confidence > 0.8:
                response += f"\n\n🎯 **AI Asistent:** Moja analiza je {nlp_result.confidence * 100}% sigurna!"
            
            return response
            
        except Exception as e:
            self.logger.error(f"Greška u personalizaciji odgovora: {e}")
            return template
    
    def _generate_default_response(self, user_message: str, nlp_result: NLPResult) -> str:
        """Generiše default odgovor ako nema template-a"""
        return f"""🤖 **AI Asistent - Inteligentna Podrška:**

'{user_message}' je interesantno pitanje! 🧠

**💡 Šta mogu da uradim:**
• Izvršim komande u sistemu
• Otvorim dialoge (nalozi, isplate, analiza)
• Kontrolišem platforme
• Dajem savete o zaradi

**🚀 Napredne AI funkcionalnosti:**
• Earning AI - strategije zarade
• Content AI - generisanje sadržaja
• Crypto AI - trgovanje i DeFi
• Social Media AI - viral strategije
• SEO AI - optimizacija za Google
• Analytics AI - predviđanje trendova

**💬 Preporučujem:**
• Pitajte konkretno šta želite
• Koristite komande poput 'status', 'analiza'
• Tražite AI savete o platformama ili zaradi

**Kako vam mogu pomoći sa '{user_message}'?"""
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Vraća istoriju konverzacije"""
        return self.conversation_history.copy()
    
    def clear_conversation_history(self):
        """Briše istoriju konverzacije"""
        self.conversation_history.clear()
        self.logger.info("Istorija konverzacije obrisana")

# Globalna instanca Intelligent Response Engine-a
intelligent_response_engine = IntelligentResponseEngine()

def get_intelligent_response_engine() -> IntelligentResponseEngine:
    """Vraća globalnu instancu Intelligent Response Engine-a"""
    return intelligent_response_engine

def generate_response(nlp_result: NLPResult, user_message: str = "") -> str:
    """Brza funkcija za generisanje odgovora"""
    return intelligent_response_engine.generate_response(nlp_result, user_message)
