#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - Realtime Market Predictor
Prediktor tržišta u realnom vremenu
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

class MarketTrend(Enum):
    """Market trends"""
    BULLISH = "bullish"
    BEARISH = "bearish"
    SIDEWAYS = "sideways"
    VOLATILE = "volatile"

@dataclass
class MarketPrediction:
    """Market prediction structure"""
    prediction_id: str
    platform: str
    trend: MarketTrend
    confidence: float
    predicted_earnings: float
    timeframe: str
    factors: List[str]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class MarketData:
    """Market data structure"""
    platform: str
    current_earnings: float
    historical_earnings: List[float]
    market_conditions: Dict[str, Any]
    volatility: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class RealtimeMarketPredictor:
    """Realtime Market Predictor for AutoEarnPro 2.0"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Prediction state
        self.market_data: Dict[str, MarketData] = {}
        self.predictions: List[MarketPrediction] = []
        self.prediction_callbacks: List[Callable[[MarketPrediction], None]] = []
        
        # Threading
        self.prediction_thread = None
        self.running = False
        self._lock = threading.RLock()
        
        # Supported platforms
        self.supported_platforms = [
            'textbroker', 'iwriter', 'medium', 'upwork', 'fiverr', 'freelancer',
            'surveys', 'amazon_mturk', 'clickworker', 'appen', 'lionbridge'
        ]
        
        # Market indicators
        self.market_indicators = {
            'demand_level': 0.0,
            'competition_level': 0.0,
            'seasonal_factor': 0.0,
            'economic_condition': 0.0,
            'platform_stability': 0.0
        }
        
        self.logger.info("📈 Realtime Market Predictor initialized")
    
    def start_prediction_service(self):
        """Start realtime prediction service"""
        if self.running:
            return
        
        self.running = True
        self.prediction_thread = threading.Thread(target=self._prediction_loop, daemon=True)
        self.prediction_thread.start()
        
        self.logger.info("Realtime market prediction service started")
    
    def add_prediction_callback(self, callback: Callable[[MarketPrediction], None]):
        """Add prediction callback"""
        self.prediction_callbacks.append(callback)
    
    def _prediction_loop(self):
        """Main prediction loop"""
        while self.running:
            try:
                # Update market data
                self._update_market_data()
                
                # Generate predictions
                self._generate_predictions()
                
                # Update market indicators
                self._update_market_indicators()
                
                time.sleep(300)  # Update every 5 minutes
                
            except Exception as e:
                self.logger.error(f"Error in prediction loop: {e}")
                time.sleep(60)
    
    def _update_market_data(self):
        """Update market data for all platforms"""
        try:
            for platform in self.supported_platforms:
                market_data = self._collect_platform_data(platform)
                
                with self._lock:
                    self.market_data[platform] = market_data
                
            self.logger.debug(f"Updated market data for {len(self.supported_platforms)} platforms")
            
        except Exception as e:
            self.logger.error(f"Error updating market data: {e}")
    
    def _collect_platform_data(self, platform: str) -> MarketData:
        """Collect data for a specific platform"""
        try:
            # Simulate data collection
            current_earnings = random.uniform(50, 500)
            historical_earnings = [random.uniform(30, 400) for _ in range(30)]
            volatility = random.uniform(0.1, 0.5)
            
            market_conditions = {
                'demand': random.uniform(0.3, 1.0),
                'competition': random.uniform(0.2, 0.8),
                'seasonality': random.uniform(0.5, 1.5),
                'platform_health': random.uniform(0.7, 1.0),
                'payment_speed': random.uniform(0.5, 1.0)
            }
            
            return MarketData(
                platform=platform,
                current_earnings=current_earnings,
                historical_earnings=historical_earnings,
                market_conditions=market_conditions,
                volatility=volatility
            )
            
        except Exception as e:
            self.logger.error(f"Error collecting data for {platform}: {e}")
            return MarketData(
                platform=platform,
                current_earnings=0.0,
                historical_earnings=[],
                market_conditions={},
                volatility=0.0
            )
    
    def _generate_predictions(self):
        """Generate predictions for all platforms"""
        try:
            for platform in self.supported_platforms:
                if platform in self.market_data:
                    prediction = self._predict_platform_market(platform)
                    
                    if prediction:
                        with self._lock:
                            self.predictions.append(prediction)
                            
                            # Keep predictions manageable
                            if len(self.predictions) > 1000:
                                self.predictions = self.predictions[-1000:]
                        
                        # Notify callbacks
                        self._notify_prediction_callbacks(prediction)
            
            self.logger.debug(f"Generated predictions for {len(self.supported_platforms)} platforms")
            
        except Exception as e:
            self.logger.error(f"Error generating predictions: {e}")
    
    def _predict_platform_market(self, platform: str) -> Optional[MarketPrediction]:
        """Predict market conditions for a specific platform"""
        try:
            market_data = self.market_data.get(platform)
            if not market_data:
                return None
            
            # Analyze historical data
            avg_earnings = sum(market_data.historical_earnings) / len(market_data.historical_earnings) if market_data.historical_earnings else 0
            current_earnings = market_data.current_earnings
            
            # Calculate trend
            if current_earnings > avg_earnings * 1.1:
                trend = MarketTrend.BULLISH
            elif current_earnings < avg_earnings * 0.9:
                trend = MarketTrend.BEARISH
            elif market_data.volatility > 0.3:
                trend = MarketTrend.VOLATILE
            else:
                trend = MarketTrend.SIDEWAYS
            
            # Calculate confidence
            confidence = self._calculate_prediction_confidence(market_data)
            
            # Predict future earnings
            predicted_earnings = self._predict_future_earnings(market_data, trend)
            
            # Identify factors
            factors = self._identify_market_factors(market_data, trend)
            
            prediction_id = f"pred_{int(time.time())}_{random.randint(1000, 9999)}"
            
            return MarketPrediction(
                prediction_id=prediction_id,
                platform=platform,
                trend=trend,
                confidence=confidence,
                predicted_earnings=predicted_earnings,
                timeframe="7d",
                factors=factors
            )
            
        except Exception as e:
            self.logger.error(f"Error predicting market for {platform}: {e}")
            return None
    
    def _calculate_prediction_confidence(self, market_data: MarketData) -> float:
        """Calculate confidence level for prediction"""
        try:
            # Base confidence on data quality and market stability
            data_quality = min(1.0, len(market_data.historical_earnings) / 30)
            market_stability = 1.0 - market_data.volatility
            
            # Consider market conditions
            demand_factor = market_data.market_conditions.get('demand', 0.5)
            platform_health = market_data.market_conditions.get('platform_health', 0.5)
            
            confidence = (data_quality * 0.3 + 
                         market_stability * 0.3 + 
                         demand_factor * 0.2 + 
                         platform_health * 0.2)
            
            return max(0.1, min(0.95, confidence))
            
        except Exception as e:
            self.logger.error(f"Error calculating prediction confidence: {e}")
            return 0.5
    
    def _predict_future_earnings(self, market_data: MarketData, trend: MarketTrend) -> float:
        """Predict future earnings based on trend"""
        try:
            current_earnings = market_data.current_earnings
            
            # Apply trend multiplier
            trend_multipliers = {
                MarketTrend.BULLISH: random.uniform(1.1, 1.3),
                MarketTrend.BEARISH: random.uniform(0.7, 0.9),
                MarketTrend.SIDEWAYS: random.uniform(0.95, 1.05),
                MarketTrend.VOLATILE: random.uniform(0.8, 1.2)
            }
            
            base_prediction = current_earnings * trend_multipliers.get(trend, 1.0)
            
            # Apply seasonal adjustments
            seasonal_factor = market_data.market_conditions.get('seasonality', 1.0)
            adjusted_prediction = base_prediction * seasonal_factor
            
            return max(0, adjusted_prediction)
            
        except Exception as e:
            self.logger.error(f"Error predicting future earnings: {e}")
            return market_data.current_earnings
    
    def _identify_market_factors(self, market_data: MarketData, trend: MarketTrend) -> List[str]:
        """Identify factors influencing market trend"""
        factors = []
        
        try:
            # Demand factors
            demand = market_data.market_conditions.get('demand', 0.5)
            if demand > 0.8:
                factors.append("High market demand")
            elif demand < 0.3:
                factors.append("Low market demand")
            
            # Competition factors
            competition = market_data.market_conditions.get('competition', 0.5)
            if competition > 0.7:
                factors.append("High competition")
            elif competition < 0.3:
                factors.append("Low competition")
            
            # Platform factors
            platform_health = market_data.market_conditions.get('platform_health', 0.5)
            if platform_health > 0.9:
                factors.append("Excellent platform stability")
            elif platform_health < 0.6:
                factors.append("Platform issues detected")
            
            # Volatility factors
            if market_data.volatility > 0.4:
                factors.append("High market volatility")
            elif market_data.volatility < 0.1:
                factors.append("Stable market conditions")
            
            # Trend-specific factors
            if trend == MarketTrend.BULLISH:
                factors.append("Positive market momentum")
            elif trend == MarketTrend.BEARISH:
                factors.append("Declining market conditions")
            elif trend == MarketTrend.VOLATILE:
                factors.append("Unpredictable market movements")
            
            return factors
            
        except Exception as e:
            self.logger.error(f"Error identifying market factors: {e}")
            return ["Market analysis unavailable"]
    
    def _update_market_indicators(self):
        """Update global market indicators"""
        try:
            # Calculate aggregate indicators
            total_demand = 0
            total_competition = 0
            total_stability = 0
            platform_count = 0
            
            for platform, data in self.market_data.items():
                total_demand += data.market_conditions.get('demand', 0.5)
                total_competition += data.market_conditions.get('competition', 0.5)
                total_stability += data.market_conditions.get('platform_health', 0.5)
                platform_count += 1
            
            if platform_count > 0:
                self.market_indicators['demand_level'] = total_demand / platform_count
                self.market_indicators['competition_level'] = total_competition / platform_count
                self.market_indicators['platform_stability'] = total_stability / platform_count
            
            # Update seasonal factor (simulate seasonal changes)
            current_month = datetime.now().month
            if current_month in [12, 1, 2]:  # Winter
                self.market_indicators['seasonal_factor'] = 0.8
            elif current_month in [6, 7, 8]:  # Summer
                self.market_indicators['seasonal_factor'] = 1.2
            else:  # Spring/Fall
                self.market_indicators['seasonal_factor'] = 1.0
            
            # Simulate economic conditions
            self.market_indicators['economic_condition'] = random.uniform(0.7, 1.1)
            
        except Exception as e:
            self.logger.error(f"Error updating market indicators: {e}")
    
    def _notify_prediction_callbacks(self, prediction: MarketPrediction):
        """Notify prediction callbacks"""
        for callback in self.prediction_callbacks:
            try:
                callback(prediction)
            except Exception as e:
                self.logger.error(f"Error in prediction callback: {e}")
    
    def get_latest_predictions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get latest predictions"""
        try:
            with self._lock:
                recent_predictions = self.predictions[-limit:] if self.predictions else []
                
                return [
                    {
                        'prediction_id': pred.prediction_id,
                        'platform': pred.platform,
                        'trend': pred.trend.value,
                        'confidence': pred.confidence,
                        'predicted_earnings': pred.predicted_earnings,
                        'timeframe': pred.timeframe,
                        'factors': pred.factors,
                        'timestamp': pred.timestamp.isoformat()
                    }
                    for pred in recent_predictions
                ]
                
        except Exception as e:
            self.logger.error(f"Error getting latest predictions: {e}")
            return []
    
    def get_platform_prediction(self, platform: str) -> Optional[Dict[str, Any]]:
        """Get latest prediction for a specific platform"""
        try:
            with self._lock:
                for prediction in reversed(self.predictions):
                    if prediction.platform == platform:
                        return {
                            'prediction_id': prediction.prediction_id,
                            'platform': prediction.platform,
                            'trend': prediction.trend.value,
                            'confidence': prediction.confidence,
                            'predicted_earnings': prediction.predicted_earnings,
                            'timeframe': prediction.timeframe,
                            'factors': prediction.factors,
                            'timestamp': prediction.timestamp.isoformat()
                        }
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting platform prediction for {platform}: {e}")
            return None
    
    def get_market_indicators(self) -> Dict[str, float]:
        """Get current market indicators"""
        return self.market_indicators.copy()
    
    def get_market_data(self, platform: str) -> Optional[Dict[str, Any]]:
        """Get market data for a specific platform"""
        try:
            with self._lock:
                if platform in self.market_data:
                    data = self.market_data[platform]
                    return {
                        'platform': data.platform,
                        'current_earnings': data.current_earnings,
                        'historical_earnings': data.historical_earnings,
                        'market_conditions': data.market_conditions,
                        'volatility': data.volatility,
                        'timestamp': data.timestamp.isoformat()
                    }
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting market data for {platform}: {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get prediction statistics"""
        with self._lock:
            total_predictions = len(self.predictions)
            
            # Count by trend
            trend_counts = {}
            for prediction in self.predictions:
                trend = prediction.trend.value
                trend_counts[trend] = trend_counts.get(trend, 0) + 1
            
            # Calculate average confidence
            avg_confidence = sum(p.confidence for p in self.predictions) / total_predictions if total_predictions > 0 else 0
            
            return {
                'total_predictions': total_predictions,
                'trend_distribution': trend_counts,
                'average_confidence': avg_confidence,
                'supported_platforms': len(self.supported_platforms),
                'prediction_service_active': self.running
            }
    
    def shutdown(self):
        """Shutdown prediction service"""
        try:
            self.running = False
            
            if self.prediction_thread:
                self.prediction_thread.join(timeout=5)
            
            self.logger.info("🔒 Realtime Market Predictor shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during prediction shutdown: {e}")

# Global market predictor instance
_global_market_predictor = None

def get_realtime_market_predictor(config: Optional[Dict[str, Any]] = None) -> RealtimeMarketPredictor:
    """Get global realtime market predictor instance"""
    global _global_market_predictor
    if _global_market_predictor is None:
        _global_market_predictor = RealtimeMarketPredictor(config)
    return _global_market_predictor
