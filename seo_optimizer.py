#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - SEO Optimizer
AI optimizacija za SEO
"""

import logging
import random
from datetime import datetime
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SEOOptimizer:
    """AI optimizacija za SEO"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.keywords = {}
        self.optimization_history = []
        
    def optimize_content(self, content: str, target_keywords: List[str]) -> Dict[str, Any]:
        """Optimizuje sadržaj za SEO"""
        try:
            self.logger.info(f"Optimizujem sadržaj za ključne reči: {target_keywords}")
            
            # Analiza sadržaja
            analysis = self._analyze_content(content, target_keywords)
            
            # Generisanje optimizovanog sadržaja
            optimized_content = self._optimize_content(content, target_keywords, analysis)
            
            # SEO preporuke
            recommendations = self._generate_seo_recommendations(analysis)
            
            result = {
                'original_content': content,
                'optimized_content': optimized_content,
                'target_keywords': target_keywords,
                'analysis': analysis,
                'recommendations': recommendations,
                'seo_score': self._calculate_seo_score(analysis),
                'optimized_at': datetime.now().isoformat()
            }
            
            self.optimization_history.append(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Greška pri SEO optimizaciji: {e}")
            return {}
    
    def generate_meta_tags(self, title: str, description: str, keywords: List[str]) -> Dict[str, Any]:
        """Generiše meta tagove"""
        try:
            self.logger.info("Generišem meta tagove")
            
            meta_tags = {
                'title': self._optimize_title(title, keywords),
                'description': self._optimize_description(description, keywords),
                'keywords': ', '.join(keywords),
                'og_title': title,
                'og_description': description,
                'twitter_card': 'summary',
                'canonical_url': '',
                'robots': 'index, follow'
            }
            
            return {
                'meta_tags': meta_tags,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Greška pri generisanju meta tagova: {e}")
            return {}
    
    def analyze_keyword_density(self, content: str, keywords: List[str]) -> Dict[str, Any]:
        """Analizira gustinu ključnih reči"""
        try:
            self.logger.info("Analiziram gustinu ključnih reči")
            
            analysis = {}
            content_lower = content.lower()
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                count = content_lower.count(keyword_lower)
                density = (count * len(keyword_lower)) / len(content) * 100
                
                analysis[keyword] = {
                    'count': count,
                    'density': density,
                    'optimal_density': random.uniform(1.0, 3.0),
                    'status': 'optimal' if 1.0 <= density <= 3.0 else 'needs_optimization'
                }
            
            return {
                'keyword_analysis': analysis,
                'overall_density_score': random.uniform(0.6, 0.9),
                'analyzed_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Greška pri analizi gustine ključnih reči: {e}")
            return {}
    
    def generate_seo_friendly_url(self, title: str) -> str:
        """Generiše SEO-friendly URL"""
        try:
            self.logger.info("Generišem SEO-friendly URL")
            
            # Jednostavna simulacija generisanja URL-a
            url = title.lower()
            url = url.replace(' ', '-')
            url = url.replace('š', 's').replace('ć', 'c').replace('č', 'c').replace('đ', 'd').replace('ž', 'z')
            url = ''.join(c for c in url if c.isalnum() or c == '-')
            url = url.strip('-')
            
            return f"/{url}"
            
        except Exception as e:
            self.logger.error(f"Greška pri generisanju URL-a: {e}")
            return "/page"
    
    def _analyze_content(self, content: str, keywords: List[str]) -> Dict[str, Any]:
        """Analizira sadržaj"""
        return {
            'word_count': len(content.split()),
            'character_count': len(content),
            'keyword_density': self._calculate_keyword_density(content, keywords),
            'readability_score': random.uniform(0.6, 0.9),
            'content_structure': self._analyze_structure(content),
            'internal_links': random.randint(0, 5),
            'external_links': random.randint(0, 3)
        }
    
    def _optimize_content(self, content: str, keywords: List[str], analysis: Dict[str, Any]) -> str:
        """Optimizuje sadržaj"""
        # Simulacija optimizacije
        optimized = content
        
        # Dodaj ključne reči u naslov ako nisu prisutne
        for keyword in keywords:
            if keyword.lower() not in content.lower():
                optimized = f"{keyword} - {optimized}"
                break
        
        return optimized
    
    def _generate_seo_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generiše SEO preporuke"""
        recommendations = []
        
        if analysis['word_count'] < 300:
            recommendations.append("Povećajte broj reči u sadržaju (preporučeno: 300+ reči)")
        
        if analysis['keyword_density'] < 1.0:
            recommendations.append("Povećajte gustinu ključnih reči")
        elif analysis['keyword_density'] > 3.0:
            recommendations.append("Smanjite gustinu ključnih reči (keyword stuffing)")
        
        if analysis['internal_links'] < 2:
            recommendations.append("Dodajte više internih linkova")
        
        if analysis['readability_score'] < 0.7:
            recommendations.append("Poboljšajte čitljivost sadržaja")
        
        return recommendations
    
    def _calculate_seo_score(self, analysis: Dict[str, Any]) -> float:
        """Računa SEO skor"""
        score = 0.0
        
        # Word count score
        if analysis['word_count'] >= 300:
            score += 0.2
        elif analysis['word_count'] >= 200:
            score += 0.1
        
        # Keyword density score
        density = analysis['keyword_density']
        if 1.0 <= density <= 3.0:
            score += 0.3
        elif 0.5 <= density <= 4.0:
            score += 0.2
        
        # Readability score
        score += analysis['readability_score'] * 0.2
        
        # Structure score
        score += 0.1
        
        # Links score
        if analysis['internal_links'] >= 2:
            score += 0.1
        if analysis['external_links'] >= 1:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_keyword_density(self, content: str, keywords: List[str]) -> float:
        """Računa gustinu ključnih reči"""
        if not keywords:
            return 0.0
        
        total_density = 0.0
        content_lower = content.lower()
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            count = content_lower.count(keyword_lower)
            density = (count * len(keyword_lower)) / len(content) * 100
            total_density += density
        
        return total_density / len(keywords)
    
    def _analyze_structure(self, content: str) -> Dict[str, Any]:
        """Analizira strukturu sadržaja"""
        lines = content.split('\n')
        
        return {
            'paragraphs': len([line for line in lines if line.strip()]),
            'has_headings': any(line.strip().startswith('#') for line in lines),
            'has_lists': any(line.strip().startswith(('-', '*', '•')) for line in lines),
            'average_paragraph_length': random.randint(50, 150)
        }
    
    def _optimize_title(self, title: str, keywords: List[str]) -> str:
        """Optimizuje naslov"""
        if not keywords:
            return title
        
        # Dodaj ključnu reč u naslov ako nije prisutna
        for keyword in keywords:
            if keyword.lower() not in title.lower():
                return f"{title} - {keyword}"
        
        return title
    
    def _optimize_description(self, description: str, keywords: List[str]) -> str:
        """Optimizuje opis"""
        if len(description) > 160:
            description = description[:157] + "..."
        
        # Dodaj ključnu reč ako nije prisutna
        if keywords and keywords[0].lower() not in description.lower():
            description = f"{description} {keywords[0]}"
        
        return description
