"""
Predictive Analytics Suite - Advanced predictive modeling and analysis
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report


class ModelType(Enum):
    """Available model types"""
    LINEAR_REGRESSION = "linear_regression"
    LOGISTIC_REGRESSION = "logistic_regression"
    RANDOM_FOREST_REGRESSION = "random_forest_regression"
    RANDOM_FOREST_CLASSIFICATION = "random_forest_classification"
    TIME_SERIES = "time_series"
    CLUSTERING = "clustering"


class PredictionType(Enum):
    """Prediction types"""
    REGRESSION = "regression"
    CLASSIFICATION = "classification"
    FORECASTING = "forecasting"
    ANOMALY_DETECTION = "anomaly_detection"


@dataclass
class PredictionResult:
    """Prediction result"""
    target: str
    predicted_value: Any
    confidence: float
    model_type: ModelType
    timestamp: datetime
    features_used: List[str]
    actual_value: Optional[Any] = None


@dataclass
class ModelPerformance:
    """Model performance metrics"""
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    mse: float
    mae: float
    last_updated: datetime


class PredictiveAnalyticsSuite:
    """Advanced predictive analytics suite"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.models = {}
        self.data_sets = {}
        self.predictions = []
        self.model_performance = {}
        self.feature_importance = {}
        self.logger = logging.getLogger(__name__)
        self.scaler = StandardScaler()
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize predictive models"""
        try:
            for model_type in ModelType:
                self.models[model_type] = {
                    'model': None,
                    'trained': False,
                    'last_training': None,
                    'parameters': self._get_default_parameters(model_type)
                }
            
            self.logger.info("Predictive models initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing models: {e}")
    
    def _get_default_parameters(self, model_type: ModelType) -> Dict:
        """Get default parameters for model type"""
        params = {
            ModelType.LINEAR_REGRESSION: {
                'fit_intercept': True,
                'normalize': False
            },
            ModelType.LOGISTIC_REGRESSION: {
                'C': 1.0,
                'max_iter': 1000,
                'random_state': 42
            },
            ModelType.RANDOM_FOREST_REGRESSION: {
                'n_estimators': 100,
                'max_depth': 10,
                'random_state': 42
            },
            ModelType.RANDOM_FOREST_CLASSIFICATION: {
                'n_estimators': 100,
                'max_depth': 10,
                'random_state': 42
            },
            ModelType.TIME_SERIES: {
                'window_size': 30,
                'forecast_horizon': 7
            },
            ModelType.CLUSTERING: {
                'n_clusters': 3,
                'random_state': 42
            }
        }
        return params.get(model_type, {})
    
    def add_dataset(self, name: str, data: pd.DataFrame, target_column: str) -> bool:
        """Add a dataset for analysis"""
        try:
            if target_column not in data.columns:
                self.logger.error(f"Target column {target_column} not found in dataset")
                return False
            
            self.data_sets[name] = {
                'data': data.copy(),
                'target_column': target_column,
                'features': [col for col in data.columns if col != target_column],
                'added_date': datetime.now()
            }
            
            self.logger.info(f"Dataset {name} added successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error adding dataset {name}: {e}")
            return False
    
    def train_model(self, dataset_name: str, model_type: ModelType, 
                   target_column: Optional[str] = None) -> bool:
        """Train a predictive model"""
        try:
            if dataset_name not in self.data_sets:
                self.logger.error(f"Dataset {dataset_name} not found")
                return False
            
            dataset = self.data_sets[dataset_name]
            data = dataset['data']
            target_col = target_column or dataset['target_column']
            
            # Prepare features and target
            X = data.drop(columns=[target_col])
            y = data[target_col]
            
            # Handle missing values
            X = X.fillna(X.mean())
            y = y.fillna(y.mean())
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Create and train model
            model = self._create_model(model_type)
            if model is None:
                return False
            
            model.fit(X_train_scaled, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test_scaled)
            
            # Calculate performance metrics
            performance = self._calculate_performance(y_test, y_pred, model_type)
            
            # Store model and performance
            self.models[model_type]['model'] = model
            self.models[model_type]['trained'] = True
            self.models[model_type]['last_training'] = datetime.now()
            
            self.model_performance[model_type] = performance
            
            # Calculate feature importance
            self._calculate_feature_importance(model, X.columns, model_type)
            
            self.logger.info(f"Model {model_type.value} trained successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error training model {model_type.value}: {e}")
            return False
    
    def _create_model(self, model_type: ModelType):
        """Create a model instance"""
        try:
            if model_type == ModelType.LINEAR_REGRESSION:
                return LinearRegression(**self.models[model_type]['parameters'])
            elif model_type == ModelType.LOGISTIC_REGRESSION:
                return LogisticRegression(**self.models[model_type]['parameters'])
            elif model_type == ModelType.RANDOM_FOREST_REGRESSION:
                return RandomForestRegressor(**self.models[model_type]['parameters'])
            elif model_type == ModelType.RANDOM_FOREST_CLASSIFICATION:
                return RandomForestClassifier(**self.models[model_type]['parameters'])
            else:
                self.logger.warning(f"Model type {model_type.value} not implemented")
                return None
        except Exception as e:
            self.logger.error(f"Error creating model {model_type.value}: {e}")
            return None
    
    def _calculate_performance(self, y_true, y_pred, model_type: ModelType) -> ModelPerformance:
        """Calculate model performance metrics"""
        try:
            mse = mean_squared_error(y_true, y_pred)
            mae = np.mean(np.abs(y_true - y_pred))
            
            if model_type in [ModelType.LOGISTIC_REGRESSION, ModelType.RANDOM_FOREST_CLASSIFICATION]:
                accuracy = accuracy_score(y_true, y_pred)
                # For classification, calculate precision, recall, f1
                from sklearn.metrics import precision_score, recall_score, f1_score
                precision = precision_score(y_true, y_pred, average='weighted')
                recall = recall_score(y_true, y_pred, average='weighted')
                f1 = f1_score(y_true, y_pred, average='weighted')
            else:
                accuracy = 1.0 - (mse / np.var(y_true))  # R-squared equivalent
                precision = recall = f1 = 0.0
            
            return ModelPerformance(
                model_name=model_type.value,
                accuracy=accuracy,
                precision=precision,
                recall=recall,
                f1_score=f1,
                mse=mse,
                mae=mae,
                last_updated=datetime.now()
            )
        except Exception as e:
            self.logger.error(f"Error calculating performance: {e}")
            return ModelPerformance(
                model_name=model_type.value,
                accuracy=0.0,
                precision=0.0,
                recall=0.0,
                f1_score=0.0,
                mse=0.0,
                mae=0.0,
                last_updated=datetime.now()
            )
    
    def _calculate_feature_importance(self, model, feature_names, model_type: ModelType):
        """Calculate feature importance"""
        try:
            if hasattr(model, 'feature_importances_'):
                importance = model.feature_importances_
            elif hasattr(model, 'coef_'):
                importance = np.abs(model.coef_)
            else:
                importance = np.ones(len(feature_names)) / len(feature_names)
            
            self.feature_importance[model_type] = dict(zip(feature_names, importance))
        except Exception as e:
            self.logger.error(f"Error calculating feature importance: {e}")
    
    def make_prediction(self, data: pd.DataFrame, model_type: ModelType, 
                       target_column: str) -> Optional[PredictionResult]:
        """Make a prediction using trained model"""
        try:
            if not self.models[model_type]['trained']:
                self.logger.error(f"Model {model_type.value} not trained")
                return None
            
            model = self.models[model_type]['model']
            if model is None:
                return None
            
            # Prepare data
            X = data.drop(columns=[target_column])
            X = X.fillna(X.mean())
            X_scaled = self.scaler.transform(X)
            
            # Make prediction
            prediction = model.predict(X_scaled)[0]
            
            # Calculate confidence (simplified)
            confidence = 0.8  # Placeholder
            
            result = PredictionResult(
                target=target_column,
                predicted_value=prediction,
                confidence=confidence,
                model_type=model_type,
                timestamp=datetime.now(),
                features_used=list(X.columns)
            )
            
            self.predictions.append(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Error making prediction: {e}")
            return None
    
    def get_model_performance(self, model_type: Optional[ModelType] = None) -> Dict:
        """Get model performance metrics"""
        if model_type:
            return {model_type.value: self.model_performance.get(model_type)}
        return {k.value: v for k, v in self.model_performance.items()}
    
    def get_feature_importance(self, model_type: ModelType) -> Dict[str, float]:
        """Get feature importance for a model"""
        return self.feature_importance.get(model_type, {})
    
    def get_prediction_history(self, limit: int = 100) -> List[PredictionResult]:
        """Get prediction history"""
        return self.predictions[-limit:]
    
    def analyze_trends(self, dataset_name: str, column: str, 
                      window_size: int = 30) -> Dict[str, Any]:
        """Analyze trends in data"""
        try:
            if dataset_name not in self.data_sets:
                return {}
            
            data = self.data_sets[dataset_name]['data']
            if column not in data.columns:
                return {}
            
            series = data[column].dropna()
            
            # Calculate trend metrics
            trend_analysis = {
                'mean': series.mean(),
                'std': series.std(),
                'trend': self._calculate_trend(series),
                'seasonality': self._detect_seasonality(series),
                'volatility': series.std() / series.mean() if series.mean() != 0 else 0,
                'last_values': series.tail(window_size).tolist()
            }
            
            return trend_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing trends: {e}")
            return {}
    
    def _calculate_trend(self, series: pd.Series) -> str:
        """Calculate trend direction"""
        try:
            if len(series) < 2:
                return "insufficient_data"
            
            # Simple linear trend
            x = np.arange(len(series))
            slope = np.polyfit(x, series, 1)[0]
            
            if slope > 0.01:
                return "increasing"
            elif slope < -0.01:
                return "decreasing"
            else:
                return "stable"
        except Exception:
            return "unknown"
    
    def _detect_seasonality(self, series: pd.Series) -> bool:
        """Detect seasonality in time series"""
        try:
            if len(series) < 50:
                return False
            
            # Simple seasonality detection using autocorrelation
            autocorr = series.autocorr()
            return abs(autocorr) > 0.3
        except Exception:
            return False
    
    def export_model(self, model_type: ModelType, filepath: str) -> bool:
        """Export trained model"""
        try:
            if not self.models[model_type]['trained']:
                return False
            
            import joblib
            model_data = {
                'model': self.models[model_type]['model'],
                'scaler': self.scaler,
                'performance': self.model_performance.get(model_type),
                'feature_importance': self.feature_importance.get(model_type, {})
            }
            
            joblib.dump(model_data, filepath)
            self.logger.info(f"Model exported to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting model: {e}")
            return False
    
    def clear_old_predictions(self, days: int = 30) -> int:
        """Clear old predictions"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            original_count = len(self.predictions)
            
            self.predictions = [
                p for p in self.predictions
                if p.timestamp > cutoff_date
            ]
            
            cleared_count = original_count - len(self.predictions)
            self.logger.info(f"Cleared {cleared_count} old predictions")
            return cleared_count
            
        except Exception as e:
            self.logger.error(f"Error clearing old predictions: {e}")
            return 0
