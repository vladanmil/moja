#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - Crypto DeFi Engine
Motor za kriptovalute i DeFi
"""

import logging
import random
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class CryptoDefiEngine:
    """Motor za kriptovalute i DeFi"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.crypto_data = {}
        self.defi_protocols = {}
        self.trading_history = []
        self.portfolio = {}
        
    def analyze_crypto_market(self, symbols: List[str] = None) -> Dict[str, Any]:
        """Analizira kriptovalutno tržište"""
        try:
            self.logger.info("Analiziram kriptovalutno tržište")
            
            if not symbols:
                symbols = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'DOT', 'AVAX', 'MATIC']
            
            market_analysis = {}
            
            for symbol in symbols:
                # Simulacija podataka o kriptovaluti
                crypto_data = self._get_crypto_data(symbol)
                analysis = self._analyze_crypto_symbol(crypto_data)
                market_analysis[symbol] = analysis
            
            return {
                'market_overview': self._generate_market_overview(market_analysis),
                'individual_analysis': market_analysis,
                'market_sentiment': self._analyze_market_sentiment(market_analysis),
                'trend_analysis': self._analyze_market_trends(market_analysis),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Greška pri analizi kriptovalutnog tržišta: {e}")
            return {'error': str(e)}
    
    def analyze_defi_protocols(self) -> Dict[str, Any]:
        """Analizira DeFi protokole"""
        try:
            self.logger.info("Analiziram DeFi protokole")
            
            protocols = [
                'Uniswap', 'Aave', 'Compound', 'MakerDAO', 'Curve', 'SushiSwap',
                'PancakeSwap', 'Yearn Finance', 'Balancer', 'Synthetix'
            ]
            
            protocol_analysis = {}
            
            for protocol in protocols:
                # Simulacija podataka o protokolu
                protocol_data = self._get_defi_protocol_data(protocol)
                analysis = self._analyze_defi_protocol(protocol_data)
                protocol_analysis[protocol] = analysis
            
            return {
                'protocol_overview': self._generate_protocol_overview(protocol_analysis),
                'individual_protocols': protocol_analysis,
                'defi_ecosystem_health': self._assess_defi_ecosystem_health(protocol_analysis),
                'yield_opportunities': self._identify_yield_opportunities(protocol_analysis),
                'risk_assessment': self._assess_defi_risks(protocol_analysis),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Greška pri analizi DeFi protokola: {e}")
            return {'error': str(e)}
    
    def generate_trading_signals(self, symbol: str, timeframe: str = '1h') -> Dict[str, Any]:
        """Generiše trading signale"""
        try:
            self.logger.info(f"Generišem trading signale za {symbol}")
            
            # Dohvatanje istorijskih podataka
            historical_data = self._get_historical_data(symbol, timeframe)
            
            # Tehnička analiza
            technical_analysis = self._perform_technical_analysis(historical_data)
            
            # Generisanje signala
            signals = self._generate_signals(technical_analysis)
            
            # Analiza rizika
            risk_analysis = self._analyze_trading_risk(symbol, signals)
            
            return {
                'symbol': symbol,
                'timeframe': timeframe,
                'signals': signals,
                'technical_analysis': technical_analysis,
                'risk_analysis': risk_analysis,
                'confidence_level': self._calculate_signal_confidence(signals),
                'signal_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Greška pri generisanju trading signala: {e}")
            return {'error': str(e)}
    
    def optimize_defi_portfolio(self, current_portfolio: Dict[str, Any], risk_tolerance: str = 'moderate') -> Dict[str, Any]:
        """Optimizuje DeFi portfolio"""
        try:
            self.logger.info("Optimizujem DeFi portfolio")
            
            # Analiza trenutnog portfolija
            portfolio_analysis = self._analyze_current_portfolio(current_portfolio)
            
            # Identifikacija prilika
            opportunities = self._identify_defi_opportunities()
            
            # Generisanje optimizacijskih preporuka
            optimization_recommendations = self._generate_optimization_recommendations(
                portfolio_analysis, opportunities, risk_tolerance
            )
            
            # Simulacija optimizovanog portfolija
            optimized_portfolio = self._simulate_optimized_portfolio(
                current_portfolio, optimization_recommendations
            )
            
            return {
                'current_portfolio_analysis': portfolio_analysis,
                'optimization_recommendations': optimization_recommendations,
                'optimized_portfolio': optimized_portfolio,
                'expected_improvements': self._calculate_expected_improvements(
                    portfolio_analysis, optimized_portfolio
                ),
                'risk_adjustments': self._calculate_risk_adjustments(risk_tolerance),
                'optimization_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Greška pri optimizaciji portfolija: {e}")
            return {'error': str(e)}
    
    def predict_crypto_movements(self, symbol: str, prediction_horizon: str = '7d') -> Dict[str, Any]:
        """Predviđa kretanja kriptovaluta"""
        try:
            self.logger.info(f"Predviđam kretanja za {symbol}")
            
            # Analiza istorijskih podataka
            historical_data = self._get_extended_historical_data(symbol)
            
            # Analiza pattern-a
            pattern_analysis = self._analyze_price_patterns(historical_data)
            
            # Predviđanje na osnovu tehničkih indikatora
            technical_prediction = self._generate_technical_prediction(historical_data)
            
            # Predviđanje na osnovu sentiment analize
            sentiment_prediction = self._generate_sentiment_prediction(symbol)
            
            # Kombinovanje predviđanja
            combined_prediction = self._combine_predictions(technical_prediction, sentiment_prediction)
            
            return {
                'symbol': symbol,
                'prediction_horizon': prediction_horizon,
                'technical_prediction': technical_prediction,
                'sentiment_prediction': sentiment_prediction,
                'combined_prediction': combined_prediction,
                'confidence_intervals': self._calculate_confidence_intervals(combined_prediction),
                'risk_factors': self._identify_prediction_risk_factors(symbol),
                'prediction_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Greška pri predviđanju kretanja: {e}")
            return {'error': str(e)}
    
    def _get_crypto_data(self, symbol: str) -> Dict[str, Any]:
        """Dohvata podatke o kriptovaluti"""
        return {
            'symbol': symbol,
            'price': random.uniform(100, 50000),
            'market_cap': random.uniform(1e9, 1e12),
            'volume_24h': random.uniform(1e6, 1e9),
            'price_change_24h': random.uniform(-0.2, 0.2),
            'price_change_7d': random.uniform(-0.3, 0.3),
            'price_change_30d': random.uniform(-0.5, 0.5),
            'circulating_supply': random.uniform(1e6, 1e9),
            'max_supply': random.uniform(1e6, 1e9),
            'dominance': random.uniform(0.1, 50.0)
        }
    
    def _analyze_crypto_symbol(self, crypto_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizira pojedinačnu kriptovalutu"""
        return {
            'price_analysis': {
                'current_price': crypto_data['price'],
                'price_trend': 'bullish' if crypto_data['price_change_24h'] > 0 else 'bearish',
                'volatility': abs(crypto_data['price_change_24h']),
                'support_level': crypto_data['price'] * 0.9,
                'resistance_level': crypto_data['price'] * 1.1
            },
            'market_analysis': {
                'market_cap_rank': self._calculate_market_cap_rank(crypto_data['market_cap']),
                'volume_analysis': self._analyze_volume(crypto_data['volume_24h']),
                'liquidity_score': self._calculate_liquidity_score(crypto_data)
            },
            'technical_indicators': {
                'rsi': random.uniform(20, 80),
                'macd': random.uniform(-2, 2),
                'bollinger_bands': {
                    'upper': crypto_data['price'] * 1.05,
                    'middle': crypto_data['price'],
                    'lower': crypto_data['price'] * 0.95
                }
            },
            'risk_assessment': {
                'risk_level': self._assess_crypto_risk(crypto_data),
                'volatility_rating': 'high' if abs(crypto_data['price_change_24h']) > 0.1 else 'medium',
                'liquidity_rating': 'high' if crypto_data['volume_24h'] > 1e8 else 'medium'
            }
        }
    
    def _get_defi_protocol_data(self, protocol: str) -> Dict[str, Any]:
        """Dohvata podatke o DeFi protokolu"""
        return {
            'name': protocol,
            'total_value_locked': random.uniform(1e6, 1e10),
            'daily_volume': random.uniform(1e5, 1e8),
            'apy': random.uniform(0.05, 0.5),
            'user_count': random.randint(1000, 100000),
            'security_score': random.uniform(0.7, 1.0),
            'audit_status': random.choice(['audited', 'unaudited', 'partially_audited']),
            'age_days': random.randint(30, 1000),
            'tokens_supported': random.randint(10, 100)
        }
    
    def _analyze_defi_protocol(self, protocol_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizira DeFi protokol"""
        return {
            'performance_metrics': {
                'tvl_trend': 'increasing' if random.random() > 0.5 else 'decreasing',
                'volume_efficiency': protocol_data['daily_volume'] / protocol_data['total_value_locked'],
                'user_growth': random.uniform(0.01, 0.1),
                'apy_stability': random.uniform(0.8, 1.0)
            },
            'security_analysis': {
                'security_score': protocol_data['security_score'],
                'audit_quality': self._assess_audit_quality(protocol_data['audit_status']),
                'risk_factors': self._identify_protocol_risks(protocol_data),
                'insurance_coverage': random.choice([True, False])
            },
            'yield_analysis': {
                'current_apy': protocol_data['apy'],
                'apy_trend': random.choice(['stable', 'increasing', 'decreasing']),
                'yield_sustainability': self._assess_yield_sustainability(protocol_data),
                'risk_adjusted_yield': protocol_data['apy'] * protocol_data['security_score']
            },
            'ecosystem_integration': {
                'integration_score': random.uniform(0.5, 1.0),
                'partnerships': random.randint(5, 50),
                'cross_chain_support': random.choice([True, False])
            }
        }
    
    def _get_historical_data(self, symbol: str, timeframe: str) -> List[Dict[str, Any]]:
        """Dohvata istorijske podatke"""
        data_points = []
        current_price = random.uniform(100, 50000)
        
        for i in range(100):
            timestamp = datetime.now() - timedelta(hours=i)
            price_change = random.uniform(-0.05, 0.05)
            current_price *= (1 + price_change)
            
            data_points.append({
                'timestamp': timestamp,
                'open': current_price,
                'high': current_price * random.uniform(1.0, 1.02),
                'low': current_price * random.uniform(0.98, 1.0),
                'close': current_price,
                'volume': random.uniform(1e6, 1e8)
            })
        
        return data_points[::-1]  # Reverse to get chronological order
    
    def _perform_technical_analysis(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Izvršava tehničku analizu"""
        if not historical_data:
            return {}
        
        prices = [point['close'] for point in historical_data]
        volumes = [point['volume'] for point in historical_data]
        
        return {
            'moving_averages': {
                'sma_20': sum(prices[-20:]) / 20 if len(prices) >= 20 else sum(prices) / len(prices),
                'sma_50': sum(prices[-50:]) / 50 if len(prices) >= 50 else sum(prices) / len(prices),
                'ema_12': self._calculate_ema(prices, 12),
                'ema_26': self._calculate_ema(prices, 26)
            },
            'momentum_indicators': {
                'rsi': self._calculate_rsi(prices),
                'macd': self._calculate_macd(prices),
                'stochastic': self._calculate_stochastic(historical_data)
            },
            'volume_indicators': {
                'volume_sma': sum(volumes[-20:]) / 20 if len(volumes) >= 20 else sum(volumes) / len(volumes),
                'volume_trend': 'increasing' if volumes[-1] > volumes[-5] else 'decreasing'
            },
            'support_resistance': {
                'support': min(prices[-20:]) if len(prices) >= 20 else min(prices),
                'resistance': max(prices[-20:]) if len(prices) >= 20 else max(prices)
            }
        }
    
    def _generate_signals(self, technical_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generiše trading signale"""
        signals = []
        
        # RSI signali
        rsi = technical_analysis.get('momentum_indicators', {}).get('rsi', 50)
        if rsi < 30:
            signals.append({
                'type': 'buy',
                'indicator': 'RSI',
                'strength': 'strong',
                'reason': 'Oversold condition',
                'confidence': 0.8
            })
        elif rsi > 70:
            signals.append({
                'type': 'sell',
                'indicator': 'RSI',
                'strength': 'strong',
                'reason': 'Overbought condition',
                'confidence': 0.8
            })
        
        # MACD signali
        macd = technical_analysis.get('momentum_indicators', {}).get('macd', 0)
        if macd > 0:
            signals.append({
                'type': 'buy',
                'indicator': 'MACD',
                'strength': 'medium',
                'reason': 'Positive MACD',
                'confidence': 0.6
            })
        elif macd < 0:
            signals.append({
                'type': 'sell',
                'indicator': 'MACD',
                'strength': 'medium',
                'reason': 'Negative MACD',
                'confidence': 0.6
            })
        
        # Moving average signali
        sma_20 = technical_analysis.get('moving_averages', {}).get('sma_20', 0)
        sma_50 = technical_analysis.get('moving_averages', {}).get('sma_50', 0)
        
        if sma_20 > sma_50:
            signals.append({
                'type': 'buy',
                'indicator': 'Moving Average',
                'strength': 'weak',
                'reason': 'Golden cross',
                'confidence': 0.4
            })
        elif sma_20 < sma_50:
            signals.append({
                'type': 'sell',
                'indicator': 'Moving Average',
                'strength': 'weak',
                'reason': 'Death cross',
                'confidence': 0.4
            })
        
        return signals
    
    def _analyze_trading_risk(self, symbol: str, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analizira rizik trgovanja"""
        buy_signals = [s for s in signals if s['type'] == 'buy']
        sell_signals = [s for s in signals if s['type'] == 'sell']
        
        return {
            'signal_balance': len(buy_signals) - len(sell_signals),
            'overall_confidence': sum(s['confidence'] for s in signals) / len(signals) if signals else 0,
            'risk_level': 'high' if len(signals) > 5 else 'medium' if len(signals) > 2 else 'low',
            'market_volatility': random.uniform(0.1, 0.5),
            'liquidity_risk': 'low' if random.random() > 0.3 else 'medium'
        }
    
    def _calculate_signal_confidence(self, signals: List[Dict[str, Any]]) -> float:
        """Računa nivo pouzdanosti signala"""
        if not signals:
            return 0.0
        
        # Ponderisana sredina pouzdanosti
        total_confidence = sum(s['confidence'] for s in signals)
        return total_confidence / len(signals)
    
    def _analyze_current_portfolio(self, portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """Analizira trenutni portfolio"""
        total_value = sum(asset.get('value', 0) for asset in portfolio.get('assets', []))
        
        return {
            'total_value': total_value,
            'diversification_score': self._calculate_diversification_score(portfolio),
            'risk_score': self._calculate_portfolio_risk(portfolio),
            'yield_score': self._calculate_portfolio_yield(portfolio),
            'asset_allocation': self._analyze_asset_allocation(portfolio),
            'performance_metrics': self._calculate_portfolio_performance(portfolio)
        }
    
    def _identify_defi_opportunities(self) -> List[Dict[str, Any]]:
        """Identifikuje DeFi prilike"""
        opportunities = []
        
        protocols = ['Uniswap', 'Aave', 'Compound', 'Curve', 'Yearn Finance']
        
        for protocol in protocols:
            opportunities.append({
                'protocol': protocol,
                'opportunity_type': random.choice(['yield_farming', 'liquidity_provision', 'lending']),
                'expected_apy': random.uniform(0.1, 0.8),
                'risk_level': random.choice(['low', 'medium', 'high']),
                'minimum_investment': random.uniform(100, 10000),
                'liquidity': random.choice(['high', 'medium', 'low'])
            })
        
        return opportunities
    
    def _generate_optimization_recommendations(self, portfolio_analysis: Dict[str, Any], opportunities: List[Dict[str, Any]], risk_tolerance: str) -> List[Dict[str, Any]]:
        """Generiše preporuke za optimizaciju"""
        recommendations = []
        
        # Preporuke na osnovu diversifikacije
        if portfolio_analysis['diversification_score'] < 0.7:
            recommendations.append({
                'type': 'diversification',
                'priority': 'high',
                'description': 'Povećajte diversifikaciju portfolija',
                'expected_impact': 'Smanjenje rizika'
            })
        
        # Preporuke na osnovu prilika
        for opportunity in opportunities:
            if opportunity['risk_level'] == risk_tolerance and opportunity['expected_apy'] > 0.2:
                recommendations.append({
                    'type': 'yield_optimization',
                    'priority': 'medium',
                    'description': f"Razmotrite {opportunity['protocol']} za {opportunity['opportunity_type']}",
                    'expected_impact': f"Povećanje prinosa do {opportunity['expected_apy']:.1%}"
                })
        
        return recommendations
    
    def _simulate_optimized_portfolio(self, current_portfolio: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulira optimizovan portfolio"""
        optimized_assets = current_portfolio.get('assets', []).copy()
        
        # Primeni preporuke
        for rec in recommendations:
            if rec['type'] == 'yield_optimization':
                # Dodaj novu poziciju
                optimized_assets.append({
                    'protocol': 'New Protocol',
                    'value': random.uniform(1000, 5000),
                    'apy': random.uniform(0.2, 0.5),
                    'risk_level': 'medium'
                })
        
        return {
            'assets': optimized_assets,
            'total_value': sum(asset.get('value', 0) for asset in optimized_assets),
            'expected_yield': sum(asset.get('value', 0) * asset.get('apy', 0) for asset in optimized_assets),
            'diversification_score': self._calculate_diversification_score({'assets': optimized_assets})
        }
    
    def _calculate_expected_improvements(self, current_analysis: Dict[str, Any], optimized_portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """Računa očekivana poboljšanja"""
        return {
            'yield_improvement': optimized_portfolio['expected_yield'] - current_analysis.get('yield_score', 0),
            'diversification_improvement': optimized_portfolio['diversification_score'] - current_analysis.get('diversification_score', 0),
            'risk_reduction': current_analysis.get('risk_score', 0) - random.uniform(0.1, 0.3)
        }
    
    def _calculate_risk_adjustments(self, risk_tolerance: str) -> Dict[str, Any]:
        """Računa prilagodbe rizika"""
        adjustments = {
            'low': {'max_position_size': 0.1, 'max_protocol_exposure': 0.2},
            'moderate': {'max_position_size': 0.2, 'max_protocol_exposure': 0.3},
            'high': {'max_position_size': 0.3, 'max_protocol_exposure': 0.4}
        }
        
        return adjustments.get(risk_tolerance, adjustments['moderate'])
    
    def _get_extended_historical_data(self, symbol: str) -> List[Dict[str, Any]]:
        """Dohvata proširene istorijske podatke"""
        return self._get_historical_data(symbol, '1d')  # Extended data
    
    def _analyze_price_patterns(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analizira price pattern-e"""
        if not historical_data:
            return {}
        
        prices = [point['close'] for point in historical_data]
        
        return {
            'trend_pattern': self._identify_trend_pattern(prices),
            'support_resistance_levels': self._find_support_resistance(prices),
            'volatility_pattern': self._analyze_volatility_pattern(prices),
            'volume_pattern': self._analyze_volume_pattern(historical_data)
        }
    
    def _generate_technical_prediction(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generiše tehničko predviđanje"""
        if not historical_data:
            return {}
        
        current_price = historical_data[-1]['close']
        
        return {
            'price_prediction': {
                '1d': current_price * random.uniform(0.95, 1.05),
                '7d': current_price * random.uniform(0.9, 1.1),
                '30d': current_price * random.uniform(0.8, 1.2)
            },
            'trend_prediction': random.choice(['bullish', 'bearish', 'sideways']),
            'confidence_level': random.uniform(0.6, 0.9)
        }
    
    def _generate_sentiment_prediction(self, symbol: str) -> Dict[str, Any]:
        """Generiše sentiment predviđanje"""
        return {
            'market_sentiment': random.choice(['bullish', 'bearish', 'neutral']),
            'social_sentiment': random.uniform(-1, 1),
            'news_sentiment': random.uniform(-1, 1),
            'overall_sentiment_score': random.uniform(-1, 1)
        }
    
    def _combine_predictions(self, technical_prediction: Dict[str, Any], sentiment_prediction: Dict[str, Any]) -> Dict[str, Any]:
        """Kombinuje predviđanja"""
        technical_weight = 0.7
        sentiment_weight = 0.3
        
        combined_score = (
            technical_prediction.get('confidence_level', 0.5) * technical_weight +
            (sentiment_prediction.get('overall_sentiment_score', 0) + 1) / 2 * sentiment_weight
        )
        
        return {
            'combined_prediction': 'bullish' if combined_score > 0.6 else 'bearish' if combined_score < 0.4 else 'neutral',
            'confidence_score': combined_score,
            'prediction_strength': abs(combined_score - 0.5) * 2
        }
    
    def _calculate_confidence_intervals(self, combined_prediction: Dict[str, Any]) -> Dict[str, Any]:
        """Računa intervale pouzdanosti"""
        confidence = combined_prediction.get('confidence_score', 0.5)
        
        return {
            'lower_bound': confidence - 0.1,
            'upper_bound': confidence + 0.1,
            'confidence_interval': 0.2
        }
    
    def _identify_prediction_risk_factors(self, symbol: str) -> List[str]:
        """Identifikuje faktore rizika za predviđanje"""
        risk_factors = [
            'Market volatility',
            'Regulatory uncertainty',
            'Technical issues',
            'Liquidity concerns'
        ]
        
        return random.sample(risk_factors, random.randint(1, len(risk_factors)))
    
    # Helper methods
    def _calculate_market_cap_rank(self, market_cap: float) -> int:
        """Računa rang po market cap-u"""
        if market_cap > 1e11:
            return random.randint(1, 10)
        elif market_cap > 1e10:
            return random.randint(11, 50)
        elif market_cap > 1e9:
            return random.randint(51, 100)
        else:
            return random.randint(101, 500)
    
    def _analyze_volume(self, volume: float) -> Dict[str, Any]:
        """Analizira volumen"""
        return {
            'volume_level': 'high' if volume > 1e8 else 'medium' if volume > 1e7 else 'low',
            'volume_trend': random.choice(['increasing', 'decreasing', 'stable'])
        }
    
    def _calculate_liquidity_score(self, crypto_data: Dict[str, Any]) -> float:
        """Računa skor likvidnosti"""
        volume_ratio = crypto_data['volume_24h'] / crypto_data['market_cap']
        return min(volume_ratio * 100, 1.0)
    
    def _assess_crypto_risk(self, crypto_data: Dict[str, Any]) -> str:
        """Procjenjuje rizik kriptovalute"""
        volatility = abs(crypto_data['price_change_24h'])
        
        if volatility > 0.15:
            return 'high'
        elif volatility > 0.08:
            return 'medium'
        else:
            return 'low'
    
    def _assess_audit_quality(self, audit_status: str) -> str:
        """Procjenjuje kvalitet audita"""
        quality_map = {
            'audited': 'high',
            'partially_audited': 'medium',
            'unaudited': 'low'
        }
        return quality_map.get(audit_status, 'unknown')
    
    def _identify_protocol_risks(self, protocol_data: Dict[str, Any]) -> List[str]:
        """Identifikuje rizike protokola"""
        risks = []
        
        if protocol_data['audit_status'] == 'unaudited':
            risks.append('Unaudited code')
        
        if protocol_data['security_score'] < 0.8:
            risks.append('Low security score')
        
        if protocol_data['age_days'] < 100:
            risks.append('New protocol')
        
        return risks
    
    def _assess_yield_sustainability(self, protocol_data: Dict[str, Any]) -> str:
        """Procjenjuje održivost prinosa"""
        if protocol_data['apy'] > 0.3:
            return 'unsustainable'
        elif protocol_data['apy'] > 0.15:
            return 'moderate'
        else:
            return 'sustainable'
    
    def _calculate_ema(self, prices: List[float], period: int) -> float:
        """Računa EMA"""
        if len(prices) < period:
            return sum(prices) / len(prices)
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    def _calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Računa RSI"""
        if len(prices) < period + 1:
            return 50.0
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _calculate_macd(self, prices: List[float]) -> float:
        """Računa MACD"""
        if len(prices) < 26:
            return 0.0
        
        ema_12 = self._calculate_ema(prices, 12)
        ema_26 = self._calculate_ema(prices, 26)
        
        return ema_12 - ema_26
    
    def _calculate_stochastic(self, historical_data: List[Dict[str, Any]], period: int = 14) -> float:
        """Računa Stochastic oscillator"""
        if len(historical_data) < period:
            return 50.0
        
        recent_data = historical_data[-period:]
        highest_high = max(point['high'] for point in recent_data)
        lowest_low = min(point['low'] for point in recent_data)
        current_close = recent_data[-1]['close']
        
        if highest_high == lowest_low:
            return 50.0
        
        k_percent = ((current_close - lowest_low) / (highest_high - lowest_low)) * 100
        return k_percent
    
    def _calculate_diversification_score(self, portfolio: Dict[str, Any]) -> float:
        """Računa skor diversifikacije"""
        assets = portfolio.get('assets', [])
        if not assets:
            return 0.0
        
        total_value = sum(asset.get('value', 0) for asset in assets)
        if total_value == 0:
            return 0.0
        
        # Herfindahl-Hirschman Index
        concentrations = [(asset.get('value', 0) / total_value) ** 2 for asset in assets]
        hhi = sum(concentrations)
        
        # Normalizovano na 0-1 skalu (1 = potpuno diverzifikovano)
        return max(0, 1 - hhi)
    
    def _calculate_portfolio_risk(self, portfolio: Dict[str, Any]) -> float:
        """Računa rizik portfolija"""
        assets = portfolio.get('assets', [])
        if not assets:
            return 0.0
        
        risk_scores = []
        for asset in assets:
            risk_level = asset.get('risk_level', 'medium')
            risk_score = {'low': 0.2, 'medium': 0.5, 'high': 0.8}.get(risk_level, 0.5)
            weight = asset.get('value', 0) / sum(a.get('value', 0) for a in assets)
            risk_scores.append(risk_score * weight)
        
        return sum(risk_scores)
    
    def _calculate_portfolio_yield(self, portfolio: Dict[str, Any]) -> float:
        """Računa prinos portfolija"""
        assets = portfolio.get('assets', [])
        if not assets:
            return 0.0
        
        total_value = sum(asset.get('value', 0) for asset in assets)
        if total_value == 0:
            return 0.0
        
        weighted_yield = sum(asset.get('value', 0) * asset.get('apy', 0) for asset in assets)
        return weighted_yield / total_value
    
    def _analyze_asset_allocation(self, portfolio: Dict[str, Any]) -> Dict[str, float]:
        """Analizira alokaciju aktivnih sredstava"""
        assets = portfolio.get('assets', [])
        if not assets:
            return {}
        
        total_value = sum(asset.get('value', 0) for asset in assets)
        if total_value == 0:
            return {}
        
        allocation = {}
        for asset in assets:
            protocol = asset.get('protocol', 'Unknown')
            allocation[protocol] = asset.get('value', 0) / total_value
        
        return allocation
    
    def _calculate_portfolio_performance(self, portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """Računa performanse portfolija"""
        return {
            'total_return': random.uniform(-0.2, 0.5),
            'volatility': random.uniform(0.1, 0.3),
            'sharpe_ratio': random.uniform(0.5, 2.0),
            'max_drawdown': random.uniform(-0.3, -0.05)
        }
    
    def _identify_trend_pattern(self, prices: List[float]) -> str:
        """Identifikuje trend pattern"""
        if len(prices) < 10:
            return 'unknown'
        
        recent_prices = prices[-10:]
        trend = sum(1 for i in range(1, len(recent_prices)) if recent_prices[i] > recent_prices[i-1])
        
        if trend > 6:
            return 'strong_uptrend'
        elif trend > 4:
            return 'uptrend'
        elif trend < 4:
            return 'downtrend'
        else:
            return 'sideways'
    
    def _find_support_resistance(self, prices: List[float]) -> Dict[str, float]:
        """Pronalazi support i resistance nivoe"""
        if len(prices) < 20:
            return {'support': min(prices), 'resistance': max(prices)}
        
        recent_prices = prices[-20:]
        return {
            'support': min(recent_prices),
            'resistance': max(recent_prices)
        }
    
    def _analyze_volatility_pattern(self, prices: List[float]) -> str:
        """Analizira pattern volatilnosti"""
        if len(prices) < 10:
            return 'unknown'
        
        returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
        volatility = sum(abs(ret) for ret in returns) / len(returns)
        
        if volatility > 0.05:
            return 'high_volatility'
        elif volatility > 0.02:
            return 'medium_volatility'
        else:
            return 'low_volatility'
    
    def _analyze_volume_pattern(self, historical_data: List[Dict[str, Any]]) -> str:
        """Analizira pattern volumena"""
        if len(historical_data) < 10:
            return 'unknown'
        
        volumes = [point['volume'] for point in historical_data[-10:]]
        avg_volume = sum(volumes) / len(volumes)
        current_volume = volumes[-1]
        
        if current_volume > avg_volume * 1.5:
            return 'high_volume'
        elif current_volume < avg_volume * 0.5:
            return 'low_volume'
        else:
            return 'normal_volume'
