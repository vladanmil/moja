#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - Banking Advisor
Finansijski savetnik
"""

import logging
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class BankingAdvisor:
    """Finansijski savetnik"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.financial_data = {}
        self.advice_history = []
        self.risk_profiles = {}
        
    def analyze_financial_health(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizira finansijsko zdravlje"""
        try:
            self.logger.info("Analiziram finansijsko zdravlje")
            
            # Analiza prihoda i rashoda
            income_analysis = self._analyze_income(financial_data.get('income', {}))
            expense_analysis = self._analyze_expenses(financial_data.get('expenses', {}))
            
            # Analiza štednje
            savings_analysis = self._analyze_savings(financial_data.get('savings', {}))
            
            # Analiza dugova
            debt_analysis = self._analyze_debts(financial_data.get('debts', {}))
            
            # Izračunavanje finansijskog skora
            financial_score = self._calculate_financial_score(income_analysis, expense_analysis, savings_analysis, debt_analysis)
            
            return {
                'financial_score': financial_score,
                'income_analysis': income_analysis,
                'expense_analysis': expense_analysis,
                'savings_analysis': savings_analysis,
                'debt_analysis': debt_analysis,
                'recommendations': self._generate_recommendations(financial_score),
                'risk_level': self._assess_risk_level(financial_score),
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Greška pri analizi finansijskog zdravlja: {e}")
            return {'error': str(e)}
    
    def provide_investment_advice(self, investment_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Pruža savete za investiranje"""
        try:
            self.logger.info("Pružam savete za investiranje")
            
            risk_tolerance = investment_profile.get('risk_tolerance', 'moderate')
            investment_amount = investment_profile.get('amount', 1000)
            time_horizon = investment_profile.get('time_horizon', 'medium')
            
            # Generisanje investicionih preporuka
            recommendations = self._generate_investment_recommendations(risk_tolerance, investment_amount, time_horizon)
            
            # Analiza rizika
            risk_analysis = self._analyze_investment_risk(recommendations)
            
            # Predviđanje prinosa
            return_prediction = self._predict_returns(recommendations, time_horizon)
            
            return {
                'recommendations': recommendations,
                'risk_analysis': risk_analysis,
                'return_prediction': return_prediction,
                'diversification_strategy': self._create_diversification_strategy(recommendations),
                'advice_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Greška pri pružanju investicionih saveta: {e}")
            return {'error': str(e)}
    
    def create_budget_plan(self, financial_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Kreira plan budžeta"""
        try:
            self.logger.info("Kreiram plan budžeta")
            
            monthly_income = financial_goals.get('monthly_income', 3000)
            goals = financial_goals.get('goals', [])
            
            # Kreiranje budžeta
            budget = self._create_monthly_budget(monthly_income, goals)
            
            # Plan štednje
            savings_plan = self._create_savings_plan(monthly_income, goals)
            
            # Plan otplate dugova
            debt_repayment_plan = self._create_debt_repayment_plan(financial_goals.get('debts', []))
            
            return {
                'monthly_budget': budget,
                'savings_plan': savings_plan,
                'debt_repayment_plan': debt_repayment_plan,
                'financial_goals': self._prioritize_goals(goals),
                'budget_created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Greška pri kreiranju plana budžeta: {e}")
            return {'error': str(e)}
    
    def get_financial_forecast(self, current_data: Dict[str, Any], months: int = 12) -> Dict[str, Any]:
        """Vraća finansijsku prognozu"""
        try:
            self.logger.info(f"Kreiram finansijsku prognozu za {months} meseci")
            
            # Analiza trenutnih trendova
            trends = self._analyze_financial_trends(current_data)
            
            # Generisanje prognoze
            forecast = self._generate_forecast(current_data, trends, months)
            
            # Analiza scenarija
            scenarios = self._analyze_scenarios(forecast)
            
            return {
                'forecast_period': months,
                'monthly_forecast': forecast,
                'trends': trends,
                'scenarios': scenarios,
                'confidence_level': self._calculate_forecast_confidence(trends),
                'forecast_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Greška pri kreiranju prognoze: {e}")
            return {'error': str(e)}
    
    def _analyze_income(self, income_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizira prihode"""
        total_income = income_data.get('total', 0)
        income_sources = income_data.get('sources', [])
        
        return {
            'total_income': total_income,
            'income_sources': income_sources,
            'income_stability': self._assess_income_stability(income_sources),
            'growth_potential': self._assess_growth_potential(income_data)
        }
    
    def _analyze_expenses(self, expense_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizira rashode"""
        total_expenses = expense_data.get('total', 0)
        expense_categories = expense_data.get('categories', {})
        
        return {
            'total_expenses': total_expenses,
            'expense_categories': expense_categories,
            'essential_expenses': self._identify_essential_expenses(expense_categories),
            'discretionary_expenses': self._identify_discretionary_expenses(expense_categories),
            'expense_efficiency': self._assess_expense_efficiency(expense_categories)
        }
    
    def _analyze_savings(self, savings_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizira štednju"""
        total_savings = savings_data.get('total', 0)
        savings_rate = savings_data.get('rate', 0)
        
        return {
            'total_savings': total_savings,
            'savings_rate': savings_rate,
            'emergency_fund': self._assess_emergency_fund(total_savings),
            'savings_goals': self._assess_savings_goals(savings_data)
        }
    
    def _analyze_debts(self, debt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizira dugove"""
        total_debt = debt_data.get('total', 0)
        debt_types = debt_data.get('types', [])
        
        return {
            'total_debt': total_debt,
            'debt_types': debt_types,
            'debt_to_income_ratio': self._calculate_debt_to_income_ratio(total_debt),
            'debt_priority': self._prioritize_debts(debt_types)
        }
    
    def _calculate_financial_score(self, income: Dict, expenses: Dict, savings: Dict, debts: Dict) -> float:
        """Računa finansijski skor"""
        score = 0.0
        
        # Prihodi (30%)
        income_score = min(income['total_income'] / 5000, 1.0) * 0.3
        score += income_score
        
        # Rashodi (25%)
        expense_ratio = expenses['total_expenses'] / income['total_income'] if income['total_income'] > 0 else 1.0
        expense_score = max(0, 1 - expense_ratio) * 0.25
        score += expense_score
        
        # Štednja (25%)
        savings_score = min(savings['savings_rate'], 0.3) / 0.3 * 0.25
        score += savings_score
        
        # Dugovi (20%)
        debt_ratio = debts['total_debt'] / income['total_income'] if income['total_income'] > 0 else 1.0
        debt_score = max(0, 1 - debt_ratio) * 0.2
        score += debt_score
        
        return min(score, 1.0)
    
    def _generate_recommendations(self, financial_score: float) -> List[str]:
        """Generiše preporuke"""
        recommendations = []
        
        if financial_score < 0.4:
            recommendations.extend([
                "Smanjite rashode",
                "Povećajte prihode",
                "Kreirajte plan otplate dugova"
            ])
        elif financial_score < 0.7:
            recommendations.extend([
                "Povećajte štednju",
                "Diverzifikujte prihode",
                "Planirajte investicije"
            ])
        else:
            recommendations.extend([
                "Nastavite sa trenutnom strategijom",
                "Razmotrite napredne investicije",
                "Planirajte za penziju"
            ])
        
        return recommendations
    
    def _assess_risk_level(self, financial_score: float) -> str:
        """Procjenjuje nivo rizika"""
        if financial_score < 0.4:
            return 'high'
        elif financial_score < 0.7:
            return 'medium'
        else:
            return 'low'
    
    def _generate_investment_recommendations(self, risk_tolerance: str, amount: float, time_horizon: str) -> List[Dict[str, Any]]:
        """Generiše investicione preporuke"""
        recommendations = []
        
        if risk_tolerance == 'low':
            recommendations.extend([
                {'type': 'bonds', 'allocation': 0.6, 'expected_return': 0.04},
                {'type': 'savings', 'allocation': 0.3, 'expected_return': 0.02},
                {'type': 'stocks', 'allocation': 0.1, 'expected_return': 0.08}
            ])
        elif risk_tolerance == 'moderate':
            recommendations.extend([
                {'type': 'stocks', 'allocation': 0.5, 'expected_return': 0.08},
                {'type': 'bonds', 'allocation': 0.3, 'expected_return': 0.04},
                {'type': 'real_estate', 'allocation': 0.2, 'expected_return': 0.06}
            ])
        else:  # high risk
            recommendations.extend([
                {'type': 'stocks', 'allocation': 0.7, 'expected_return': 0.12},
                {'type': 'crypto', 'allocation': 0.2, 'expected_return': 0.20},
                {'type': 'commodities', 'allocation': 0.1, 'expected_return': 0.10}
            ])
        
        return recommendations
    
    def _analyze_investment_risk(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analizira rizik investicija"""
        total_risk = 0.0
        
        for rec in recommendations:
            if rec['type'] == 'bonds':
                total_risk += rec['allocation'] * 0.1
            elif rec['type'] == 'stocks':
                total_risk += rec['allocation'] * 0.3
            elif rec['type'] == 'crypto':
                total_risk += rec['allocation'] * 0.8
            else:
                total_risk += rec['allocation'] * 0.2
        
        return {
            'total_risk': total_risk,
            'risk_level': 'low' if total_risk < 0.3 else 'medium' if total_risk < 0.6 else 'high',
            'risk_breakdown': {rec['type']: rec['allocation'] for rec in recommendations}
        }
    
    def _predict_returns(self, recommendations: List[Dict[str, Any]], time_horizon: str) -> Dict[str, Any]:
        """Predviđa prinose"""
        total_return = 0.0
        
        for rec in recommendations:
            total_return += rec['allocation'] * rec['expected_return']
        
        # Prilagodba za vremenski horizont
        if time_horizon == 'short':
            total_return *= 0.8
        elif time_horizon == 'long':
            total_return *= 1.2
        
        return {
            'expected_annual_return': total_return,
            'compounded_return_5y': (1 + total_return) ** 5 - 1,
            'compounded_return_10y': (1 + total_return) ** 10 - 1
        }
    
    def _create_diversification_strategy(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Kreira strategiju diverzifikacije"""
        return {
            'asset_allocation': {rec['type']: rec['allocation'] for rec in recommendations},
            'rebalancing_frequency': 'quarterly',
            'diversification_score': self._calculate_diversification_score(recommendations)
        }
    
    def _calculate_diversification_score(self, recommendations: List[Dict[str, Any]]) -> float:
        """Računa skor diverzifikacije"""
        allocations = [rec['allocation'] for rec in recommendations]
        # Herfindahl-Hirschman Index za merenje koncentracije
        hhi = sum(allocation ** 2 for allocation in allocations)
        # Normalizovano na 0-1 skalu (1 = potpuno diverzifikovano)
        return max(0, 1 - hhi)
    
    def _create_monthly_budget(self, income: float, goals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Kreira mesečni budžet"""
        essential_expenses = income * 0.5  # 50% za osnovne troškove
        discretionary_expenses = income * 0.3  # 30% za diskrecione troškove
        savings = income * 0.2  # 20% za štednju
        
        return {
            'total_income': income,
            'essential_expenses': essential_expenses,
            'discretionary_expenses': discretionary_expenses,
            'savings': savings,
            'budget_balance': 0.0
        }
    
    def _create_savings_plan(self, income: float, goals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Kreira plan štednje"""
        total_goal_amount = sum(goal.get('amount', 0) for goal in goals)
        monthly_savings = income * 0.2
        
        return {
            'monthly_savings': monthly_savings,
            'total_goals_amount': total_goal_amount,
            'time_to_achieve_goals': total_goal_amount / monthly_savings if monthly_savings > 0 else float('inf'),
            'savings_allocation': self._allocate_savings_to_goals(goals, monthly_savings)
        }
    
    def _create_debt_repayment_plan(self, debts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Kreira plan otplate dugova"""
        if not debts:
            return {'total_debt': 0, 'repayment_plan': []}
        
        # Sortiraj dugove po prioritetu (kamate)
        sorted_debts = sorted(debts, key=lambda x: x.get('interest_rate', 0), reverse=True)
        
        return {
            'total_debt': sum(debt.get('amount', 0) for debt in debts),
            'repayment_plan': sorted_debts,
            'recommended_monthly_payment': sum(debt.get('amount', 0) * 0.1 for debt in debts)
        }
    
    def _prioritize_goals(self, goals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritizuje ciljeve"""
        return sorted(goals, key=lambda x: x.get('priority', 5))
    
    def _analyze_financial_trends(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizira finansijske trendove"""
        return {
            'income_trend': 'increasing',
            'expense_trend': 'stable',
            'savings_trend': 'increasing',
            'debt_trend': 'decreasing'
        }
    
    def _generate_forecast(self, current_data: Dict[str, Any], trends: Dict[str, Any], months: int) -> List[Dict[str, Any]]:
        """Generiše prognozu"""
        forecast = []
        current_month = datetime.now()
        
        for i in range(months):
            month_date = current_month + timedelta(days=30*i)
            
            # Simulacija prognoze
            income_growth = 0.02 if trends['income_trend'] == 'increasing' else -0.01
            expense_growth = 0.01 if trends['expense_trend'] == 'increasing' else 0.0
            
            forecast.append({
                'month': month_date.strftime('%Y-%m'),
                'projected_income': current_data.get('income', 3000) * (1 + income_growth) ** (i + 1),
                'projected_expenses': current_data.get('expenses', 2000) * (1 + expense_growth) ** (i + 1),
                'projected_savings': current_data.get('savings', 500) * (1 + 0.03) ** (i + 1)
            })
        
        return forecast
    
    def _analyze_scenarios(self, forecast: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analizira scenarije"""
        return {
            'optimistic': self._calculate_scenario(forecast, 1.1),
            'realistic': self._calculate_scenario(forecast, 1.0),
            'pessimistic': self._calculate_scenario(forecast, 0.9)
        }
    
    def _calculate_scenario(self, forecast: List[Dict[str, Any]], multiplier: float) -> Dict[str, Any]:
        """Računa scenario"""
        total_income = sum(month['projected_income'] * multiplier for month in forecast)
        total_expenses = sum(month['projected_expenses'] * multiplier for month in forecast)
        total_savings = sum(month['projected_savings'] * multiplier for month in forecast)
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_savings': total_savings,
            'net_worth_change': total_savings - total_expenses
        }
    
    def _calculate_forecast_confidence(self, trends: Dict[str, Any]) -> float:
        """Računa nivo pouzdanosti prognoze"""
        # Simulacija nivoa pouzdanosti na osnovu stabilnosti trendova
        stable_trends = sum(1 for trend in trends.values() if trend == 'stable')
        return 0.5 + (stable_trends / len(trends)) * 0.4
    
    def _assess_income_stability(self, sources: List[Dict[str, Any]]) -> str:
        """Procjenjuje stabilnost prihoda"""
        if len(sources) > 2:
            return 'high'
        elif len(sources) > 1:
            return 'medium'
        else:
            return 'low'
    
    def _assess_growth_potential(self, income_data: Dict[str, Any]) -> float:
        """Procjenjuje potencijal rasta prihoda"""
        return random.uniform(0.05, 0.15)
    
    def _identify_essential_expenses(self, categories: Dict[str, Any]) -> List[str]:
        """Identifikuje osnovne troškove"""
        essential = ['housing', 'food', 'utilities', 'transportation', 'healthcare']
        return [cat for cat in essential if cat in categories]
    
    def _identify_discretionary_expenses(self, categories: Dict[str, Any]) -> List[str]:
        """Identifikuje diskrecione troškove"""
        discretionary = ['entertainment', 'dining_out', 'shopping', 'travel']
        return [cat for cat in discretionary if cat in categories]
    
    def _assess_expense_efficiency(self, categories: Dict[str, Any]) -> float:
        """Procjenjuje efikasnost troškova"""
        return random.uniform(0.6, 0.9)
    
    def _assess_emergency_fund(self, savings: float) -> str:
        """Procjenjuje fond za hitne slučajeve"""
        if savings > 10000:
            return 'excellent'
        elif savings > 5000:
            return 'good'
        elif savings > 2000:
            return 'fair'
        else:
            return 'poor'
    
    def _assess_savings_goals(self, savings_data: Dict[str, Any]) -> List[str]:
        """Procjenjuje ciljeve štednje"""
        return ['emergency_fund', 'retirement', 'vacation']
    
    def _calculate_debt_to_income_ratio(self, total_debt: float) -> float:
        """Računa odnos duga i prihoda"""
        # Simulacija prihoda
        income = 3000
        return total_debt / income if income > 0 else 1.0
    
    def _prioritize_debts(self, debt_types: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritizuje dugove"""
        return sorted(debt_types, key=lambda x: x.get('interest_rate', 0), reverse=True)
