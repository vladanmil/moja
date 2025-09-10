"""
Market Predictor Engine - Advanced market prediction and forecasting capabilities
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio


class PredictionModel(Enum):
    """Available prediction models"""
    LINEAR_REGRESSION = "linear_regression"
    RANDOM_FOREST = "random_forest"
    LSTM = "lstm"
    ARIMA = "arima"
    PROPHET = "prophet"
    ENSEMBLE = "ensemble"


class MarketTrend(Enum):
    """Market trend classifications"""
    BULLISH = "bullish"
    BEARISH = "bearish"
    SIDEWAYS = "sideways"
    VOLATILE = "volatile"


@dataclass
class PredictionResult:
    """Result of a market prediction"""
    timestamp: datetime
    predicted_value: float
    confidence: float
    model_used: PredictionModel
    trend: MarketTrend
    factors: List[str]
    timeframe: str


class MarketPredictorEngine:
    """
    Advanced market prediction engine with multiple models and analysis capabilities
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the market predictor engine"""
        self.config = config or {}
        self.models = {}
        self.historical_data = {}
        self.prediction_history = []
        self.model_performance = {}
        self.active_predictions = {}
        
        # Initialize logging
        self.logger = logging.getLogger(__name__)
        
        # Performance tracking
        self.prediction_accuracy = {}
        self.model_weights = {}
        
        # Initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize prediction models"""
        try:
            # Initialize different prediction models
            for model in PredictionModel:
                self.models[model] = self._create_model(model)
                self.model_performance[model] = {
                    'accuracy': 0.0,
                    'predictions_made': 0,
                    'last_updated': datetime.now()
                }
            
            self.logger.info("Market prediction models initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing models: {e}")
    
    def _create_model(self, model_type: PredictionModel):
        """Create a specific prediction model"""
        # Simulate model creation
        return {
            'type': model_type,
            'parameters': self._get_model_parameters(model_type),
            'trained': False,
            'last_training': None
        }
    
    def _get_model_parameters(self, model_type: PredictionModel) -> Dict:
        """Get parameters for a specific model type"""
        params = {
            PredictionModel.LINEAR_REGRESSION: {
                'window_size': 30,
                'min_samples': 50
            },
            PredictionModel.RANDOM_FOREST: {
                'n_estimators': 100,
                'max_depth': 10,
                'min_samples_split': 5
            },
            PredictionModel.LSTM: {
                'sequence_length': 60,
                'units': 50,
                'dropout': 0.2
            },
            PredictionModel.ARIMA: {
                'p': 1,
                'd': 1,
                'q': 1
            },
            PredictionModel.PROPHET: {
                'changepoint_prior_scale': 0.05,
                'seasonality_prior_scale': 10.0
            },
            PredictionModel.ENSEMBLE: {
                'weights': [0.2, 0.2, 0.2, 0.2, 0.2],
                'models': list(PredictionModel)[:-1]  # All except ensemble
            }
        }
        return params.get(model_type, {})
    
    def add_market_data(self, symbol: str, data: Dict[str, Any]) -> bool:
        """Add market data for a specific symbol"""
        try:
            if symbol not in self.historical_data:
                self.historical_data[symbol] = []
            
            # Add timestamp if not present
            if 'timestamp' not in data:
                data['timestamp'] = datetime.now()
            
            self.historical_data[symbol].append(data)
            
            # Keep only recent data (last 1000 entries)
            if len(self.historical_data[symbol]) > 1000:
                self.historical_data[symbol] = self.historical_data[symbol][-1000:]
            
            self.logger.info(f"Added market data for {symbol}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding market data for {symbol}: {e}")
            return False
    
    def predict_market_movement(self, symbol: str, timeframe: str = "1d", 
                              model: PredictionModel = PredictionModel.ENSEMBLE) -> Optional[PredictionResult]:
        """Predict market movement for a specific symbol"""
        try:
            if symbol not in self.historical_data:
                self.logger.warning(f"No historical data available for {symbol}")
                return None
            
            # Prepare data for prediction
            data = self._prepare_prediction_data(symbol, timeframe)
            if not data:
                return None
            
            # Make prediction
            prediction = self._make_prediction(data, model, timeframe)
            if prediction:
                # Store prediction
                self.prediction_history.append(prediction)
                self.active_predictions[symbol] = prediction
                
                # Update model performance
                self._update_model_performance(model, prediction)
            
            return prediction
        except Exception as e:
            self.logger.error(f"Error predicting market movement for {symbol}: {e}")
            return None
    
    def _prepare_prediction_data(self, symbol: str, timeframe: str) -> Optional[pd.DataFrame]:
        """Prepare data for prediction"""
        try:
            data = self.historical_data[symbol]
            if not data:
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Add technical indicators
            df = self._add_technical_indicators(df)
            
            # Add market sentiment features
            df = self._add_sentiment_features(df)
            
            return df
        except Exception as e:
            self.logger.error(f"Error preparing prediction data: {e}")
            return None
    
    def _add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add technical indicators to the dataframe"""
        try:
            # Simple moving averages
            df['sma_20'] = df['close'].rolling(window=20).mean()
            df['sma_50'] = df['close'].rolling(window=50).mean()
            
            # RSI
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # MACD
            exp1 = df['close'].ewm(span=12).mean()
            exp2 = df['close'].ewm(span=26).mean()
            df['macd'] = exp1 - exp2
            df['macd_signal'] = df['macd'].ewm(span=9).mean()
            
            # Bollinger Bands
            df['bb_middle'] = df['close'].rolling(window=20).mean()
            bb_std = df['close'].rolling(window=20).std()
            df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
            df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
            
            return df
        except Exception as e:
            self.logger.error(f"Error adding technical indicators: {e}")
            return df
    
    def _add_sentiment_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add sentiment-based features"""
        try:
            # Volume-based sentiment
            df['volume_sma'] = df['volume'].rolling(window=20).mean()
            df['volume_ratio'] = df['volume'] / df['volume_sma']
            
            # Price momentum
            df['price_momentum'] = df['close'].pct_change(periods=5)
            
            # Volatility
            df['volatility'] = df['close'].rolling(window=20).std()
            
            return df
        except Exception as e:
            self.logger.error(f"Error adding sentiment features: {e}")
            return df
    
    def _make_prediction(self, data: pd.DataFrame, model: PredictionModel, 
                        timeframe: str) -> Optional[PredictionResult]:
        """Make prediction using specified model"""
        try:
            # Simulate prediction based on model type
            if model == PredictionModel.ENSEMBLE:
                prediction = self._ensemble_prediction(data)
            else:
                prediction = self._single_model_prediction(data, model)
            
            if prediction:
                prediction.timestamp = datetime.now()
                prediction.model_used = model
                prediction.timeframe = timeframe
                prediction.factors = self._identify_key_factors(data)
                prediction.trend = self._classify_trend(prediction.predicted_value, data)
            
            return prediction
        except Exception as e:
            self.logger.error(f"Error making prediction: {e}")
            return None
    
    def _ensemble_prediction(self, data: pd.DataFrame) -> Optional[PredictionResult]:
        """Make ensemble prediction using multiple models"""
        try:
            predictions = []
            weights = self.model_weights.get('ensemble', [0.2] * 5)
            
            # Get predictions from individual models
            for i, model in enumerate(list(PredictionModel)[:-1]):  # Exclude ensemble
                pred = self._single_model_prediction(data, model)
                if pred:
                    predictions.append(pred.predicted_value * weights[i])
            
            if predictions:
                # Weighted average
                predicted_value = sum(predictions)
                confidence = min(0.95, 0.7 + (len(predictions) * 0.05))
                
                return PredictionResult(
                    timestamp=datetime.now(),
                    predicted_value=predicted_value,
                    confidence=confidence,
                    model_used=PredictionModel.ENSEMBLE,
                    trend=MarketTrend.SIDEWAYS,  # Will be updated
                    factors=[],
                    timeframe=""
                )
            
            return None
        except Exception as e:
            self.logger.error(f"Error in ensemble prediction: {e}")
            return None
    
    def _single_model_prediction(self, data: pd.DataFrame, model: PredictionModel) -> Optional[PredictionResult]:
        """Make prediction using a single model"""
        try:
            # Simulate model-specific predictions
            last_price = data['close'].iloc[-1]
            
            if model == PredictionModel.LINEAR_REGRESSION:
                # Simple linear trend
                slope = (data['close'].iloc[-1] - data['close'].iloc[-20]) / 20
                predicted_value = last_price + slope
                confidence = 0.75
            
            elif model == PredictionModel.RANDOM_FOREST:
                # Random forest simulation
                features = ['rsi', 'macd', 'volume_ratio', 'price_momentum']
                feature_avg = data[features].iloc[-5:].mean().mean()
                predicted_value = last_price * (1 + feature_avg * 0.01)
                confidence = 0.80
            
            elif model == PredictionModel.LSTM:
                # LSTM simulation
                sequence = data['close'].iloc[-10:].values
                trend = np.polyfit(range(len(sequence)), sequence, 1)[0]
                predicted_value = last_price + trend * 2
                confidence = 0.85
            
            elif model == PredictionModel.ARIMA:
                # ARIMA simulation
                diff = data['close'].diff().iloc[-5:].mean()
                predicted_value = last_price + diff
                confidence = 0.70
            
            elif model == PredictionModel.PROPHET:
                # Prophet simulation
                seasonal_factor = np.sin(datetime.now().timetuple().tm_yday / 365 * 2 * np.pi) * 0.02
                predicted_value = last_price * (1 + seasonal_factor)
                confidence = 0.78
            
            else:
                return None
            
            return PredictionResult(
                timestamp=datetime.now(),
                predicted_value=predicted_value,
                confidence=confidence,
                model_used=model,
                trend=MarketTrend.SIDEWAYS,  # Will be updated
                factors=[],
                timeframe=""
            )
        except Exception as e:
            self.logger.error(f"Error in single model prediction: {e}")
            return None
    
    def _identify_key_factors(self, data: pd.DataFrame) -> List[str]:
        """Identify key factors influencing the prediction"""
        factors = []
        
        try:
            # Check technical indicators
            if data['rsi'].iloc[-1] > 70:
                factors.append("Overbought condition (RSI > 70)")
            elif data['rsi'].iloc[-1] < 30:
                factors.append("Oversold condition (RSI < 30)")
            
            if data['macd'].iloc[-1] > data['macd_signal'].iloc[-1]:
                factors.append("MACD bullish crossover")
            else:
                factors.append("MACD bearish crossover")
            
            if data['volume_ratio'].iloc[-1] > 1.5:
                factors.append("High volume activity")
            
            if data['volatility'].iloc[-1] > data['volatility'].mean():
                factors.append("Above-average volatility")
            
            return factors
        except Exception as e:
            self.logger.error(f"Error identifying key factors: {e}")
            return ["Technical analysis factors"]
    
    def _classify_trend(self, predicted_value: float, data: pd.DataFrame) -> MarketTrend:
        """Classify the predicted trend"""
        try:
            current_price = data['close'].iloc[-1]
            change_percent = (predicted_value - current_price) / current_price * 100
            
            if change_percent > 2:
                return MarketTrend.BULLISH
            elif change_percent < -2:
                return MarketTrend.BEARISH
            elif abs(change_percent) < 0.5:
                return MarketTrend.SIDEWAYS
            else:
                return MarketTrend.VOLATILE
        except Exception as e:
            self.logger.error(f"Error classifying trend: {e}")
            return MarketTrend.SIDEWAYS
    
    def _update_model_performance(self, model: PredictionModel, prediction: PredictionResult):
        """Update model performance metrics"""
        try:
            if model not in self.model_performance:
                self.model_performance[model] = {
                    'accuracy': 0.0,
                    'predictions_made': 0,
                    'last_updated': datetime.now()
                }
            
            self.model_performance[model]['predictions_made'] += 1
            self.model_performance[model]['last_updated'] = datetime.now()
            
            # Update accuracy based on confidence
            current_accuracy = self.model_performance[model]['accuracy']
            new_accuracy = (current_accuracy + prediction.confidence) / 2
            self.model_performance[model]['accuracy'] = new_accuracy
            
        except Exception as e:
            self.logger.error(f"Error updating model performance: {e}")
    
    def get_prediction_history(self, symbol: Optional[str] = None, 
                             limit: int = 100) -> List[PredictionResult]:
        """Get prediction history"""
        try:
            if symbol:
                # Filter by symbol
                history = [p for p in self.prediction_history if hasattr(p, 'symbol') and p.symbol == symbol]
            else:
                history = self.prediction_history
            
            return history[-limit:]
        except Exception as e:
            self.logger.error(f"Error getting prediction history: {e}")
            return []
    
    def get_model_performance(self) -> Dict[str, Dict]:
        """Get performance metrics for all models"""
        return self.model_performance
    
    def optimize_models(self) -> bool:
        """Optimize model parameters based on performance"""
        try:
            # Analyze performance and adjust weights
            best_model = max(self.model_performance.items(), 
                           key=lambda x: x[1]['accuracy'])
            
            # Update ensemble weights
            if best_model[0] != PredictionModel.ENSEMBLE:
                self.model_weights['ensemble'] = [0.1] * 5
                model_index = list(PredictionModel).index(best_model[0])
                self.model_weights['ensemble'][model_index] = 0.5
            
            self.logger.info(f"Models optimized. Best performing model: {best_model[0]}")
            return True
        except Exception as e:
            self.logger.error(f"Error optimizing models: {e}")
            return False
    
    def clear_old_data(self, days: int = 30) -> int:
        """Clear old historical data"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            cleared_count = 0
            
            for symbol in list(self.historical_data.keys()):
                original_count = len(self.historical_data[symbol])
                self.historical_data[symbol] = [
                    data for data in self.historical_data[symbol]
                    if data.get('timestamp', datetime.now()) > cutoff_date
                ]
                cleared_count += original_count - len(self.historical_data[symbol])
            
            self.logger.info(f"Cleared {cleared_count} old data entries")
            return cleared_count
        except Exception as e:
            self.logger.error(f"Error clearing old data: {e}")
            return 0
