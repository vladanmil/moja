#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - Interactive Learning Games
Gamifikacija AI učenja i testiranja znanja
"""

import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import logging

logger = logging.getLogger(__name__)

@dataclass
class GameQuestion:
    """Pitanje za igru"""
    id: str
    question: str
    correct_answer: str
    wrong_answers: List[str]
    explanation: str
    difficulty: str  # easy, medium, hard
    category: str
    points: int

@dataclass
class UserProgress:
    """Napredak korisnika u igrama"""
    user_id: str
    game_type: str
    total_score: int
    questions_answered: int
    correct_answers: int
    streak: int
    best_streak: int
    last_played: datetime
    achievements: List[str]

@dataclass
class GameSession:
    """Sesija igre"""
    session_id: str
    user_id: str
    game_type: str
    start_time: datetime
    end_time: Optional[datetime]
    questions_answered: int
    correct_answers: int
    score: int
    time_taken: float

class InteractiveLearningGames:
    """Napredni sistem za interaktivne AI learning igre"""
    
    def __init__(self, games_file: str = "ai_learning_games.json"):
        self.games_file = games_file
        
        # Glavni podaci
        self.questions: Dict[str, GameQuestion] = {}
        self.user_progress: Dict[str, UserProgress] = {}
        self.game_sessions: Dict[str, GameSession] = {}
        
        # Game types
        self.game_types = {
            'ai_quiz': 'AI Quiz - Testiranje AI znanja',
            'platform_challenge': 'Platform Challenge - Platforme i zarada',
            'earning_strategy': 'Earning Strategy - Strategije zarade',
            'technical_knowledge': 'Technical Knowledge - Tehničko znanje',
            'ai_modules': 'AI Modules - Poznavanje AI modula'
        }
        
        # Učitaj postojeće podatke
        self._load_games_data()
        
        # Kreiraj default pitanja ako ne postoje
        if not self.questions:
            self._create_default_questions()
        
        logger.info("🎮 Interactive Learning Games uspešno inicijalizovan!")
    
    def _load_games_data(self):
        """Učitava postojeće podatke o igrama"""
        try:
            with open(self.games_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Učitaj pitanja
                for q_data in data.get('questions', []):
                    self.questions[q_data['id']] = GameQuestion(**q_data)
                
                # Učitaj user progress
                for prog_data in data.get('user_progress', []):
                    prog_data['last_played'] = datetime.fromisoformat(prog_data['last_played'])
                    self.user_progress[f"{prog_data['user_id']}_{prog_data['game_type']}"] = UserProgress(**prog_data)
                
                # Učitaj game sessions
                for sess_data in data.get('game_sessions', []):
                    sess_data['start_time'] = datetime.fromisoformat(sess_data['start_time'])
                    if sess_data['end_time']:
                        sess_data['end_time'] = datetime.fromisoformat(sess_data['end_time'])
                    self.game_sessions[sess_data['session_id']] = GameSession(**sess_data)
                
                logger.info(f"✅ Učitano {len(self.questions)} pitanja i {len(self.user_progress)} user progress-a")
                
        except FileNotFoundError:
            logger.info("📝 Kreiran novi games fajl")
        except Exception as e:
            logger.error(f"❌ Greška pri učitavanju games podataka: {e}")
    
    def _save_games_data(self):
        """Čuva podatke o igrama"""
        try:
            data = {
                'questions': [asdict(q) for q in self.questions.values()],
                'user_progress': [asdict(prog) for prog in self.user_progress.values()],
                'game_sessions': [
                    {
                        'session_id': sess.session_id,
                        'user_id': sess.user_id,
                        'game_type': sess.game_type,
                        'start_time': sess.start_time.isoformat(),
                        'end_time': sess.end_time.isoformat() if sess.end_time else None,
                        'questions_answered': sess.questions_answered,
                        'correct_answers': sess.correct_answers,
                        'score': sess.score,
                        'time_taken': sess.time_taken
                    }
                    for sess in self.game_sessions.values()
                ]
            }
            
            with open(self.games_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.debug("💾 Games podaci sačuvani")
            
        except Exception as e:
            logger.error(f"❌ Greška pri čuvanju games podataka: {e}")
    
    def _create_default_questions(self):
        """Kreira default pitanja za igre"""
        try:
            default_questions = [
                # AI Quiz pitanja
                GameQuestion(
                    id="ai_001",
                    question="Šta je NLP Engine u AI sistemu?",
                    correct_answer="Natural Language Processing engine za razumevanje prirodnog jezika",
                    wrong_answers=[
                        "Network Protocol Layer",
                        "Neural Processing Logic",
                        "Natural Programming Language"
                    ],
                    explanation="NLP Engine omogućava AI-u da razume i obrađuje prirodni jezik korisnika",
                    difficulty="easy",
                    category="ai_basics",
                    points=10
                ),
                GameQuestion(
                    id="ai_002",
                    question="Koja je glavna funkcija Memory Engine-a?",
                    correct_answer="Pamćenje i učenje iz prethodnih interakcija",
                    wrong_answers=[
                        "Brisanje memorije",
                        "Kompresija podataka",
                        "Enkripcija informacija"
                    ],
                    explanation="Memory Engine omogućava AI-u da pamti i uči iz svake interakcije",
                    difficulty="medium",
                    category="ai_memory",
                    points=15
                ),
                
                # Platform Challenge pitanja
                GameQuestion(
                    id="platform_001",
                    question="Koja platforma je najbolja za početnike?",
                    correct_answer="Textbroker - jednostavna i pouzdana",
                    wrong_answers=[
                        "Upwork - komplikovana",
                        "Fiverr - previše konkurencije",
                        "Freelancer - spor sistem"
                    ],
                    explanation="Textbroker je idealan za početnike zbog jednostavnosti i pouzdanosti",
                    difficulty="easy",
                    category="platforms",
                    points=10
                ),
                GameQuestion(
                    id="platform_002",
                    question="Koliko platformi treba koristiti za optimalnu zaradu?",
                    correct_answer="10-15 platformi za diversifikaciju",
                    wrong_answers=[
                        "1-2 platforme",
                        "5-7 platformi",
                        "20+ platformi"
                    ],
                    explanation="10-15 platformi omogućava optimalnu diversifikaciju i zaradu",
                    difficulty="medium",
                    category="earning_strategy",
                    points=15
                ),
                
                # Earning Strategy pitanja
                GameQuestion(
                    id="earning_001",
                    question="Koja je najbolja strategija za povećanje zarade?",
                    correct_answer="Diversifikacija + optimizacija + kontinuirano učenje",
                    wrong_answers=[
                        "Fokus na jednu platformu",
                        "Rad samo vikendom",
                        "Korišćenje automatskih botova"
                    ],
                    explanation="Kombinacija diversifikacije, optimizacije i kontinuiranog učenja donosi najbolje rezultate",
                    difficulty="hard",
                    category="earning_strategy",
                    points=20
                ),
                
                # Technical Knowledge pitanja
                GameQuestion(
                    id="tech_001",
                    question="Kako funkcioniše AI Hub?",
                    correct_answer="Centralni hub koji povezuje sve AI funkcionalnosti",
                    wrong_answers=[
                        "Samo za čuvanje podataka",
                        "Samo za komunikaciju",
                        "Samo za backup"
                    ],
                    explanation="AI Hub je centralni sistem koji povezuje i omogućava pristup svim AI funkcionalnostima",
                    difficulty="medium",
                    category="technical",
                    points=15
                ),
                
                # AI Modules pitanja
                GameQuestion(
                    id="modules_001",
                    question="Koliko AI modula ima AutoEarnPro?",
                    correct_answer="50+ naprednih AI modula",
                    wrong_answers=[
                        "5-10 modula",
                        "15-20 modula",
                        "25-30 modula"
                    ],
                    explanation="AutoEarnPro ima preko 50 naprednih AI modula za različite funkcionalnosti",
                    difficulty="easy",
                    category="ai_modules",
                    points=10
                )
            ]
            
            for question in default_questions:
                self.questions[question.id] = question
            
            logger.info(f"✅ Kreirano {len(default_questions)} default pitanja")
            self._save_games_data()
            
        except Exception as e:
            logger.error(f"❌ Greška pri kreiranju default pitanja: {e}")
    
    def start_ai_quiz(self, user_id: str = "default", difficulty: str = "easy", 
                      category: str = None, question_count: int = 10) -> Dict[str, Any]:
        """Pokreće AI Quiz igru"""
        try:
            # Filtriraj pitanja
            available_questions = []
            for question in self.questions.values():
                if question.difficulty == difficulty:
                    if category is None or question.category == category:
                        available_questions.append(question)
            
            if len(available_questions) < question_count:
                question_count = len(available_questions)
            
            if question_count == 0:
                return {"error": "Nema dostupnih pitanja za ovu kategoriju i težinu"}
            
            # Izaberi nasumična pitanja
            selected_questions = random.sample(available_questions, question_count)
            
            # Kreiraj game session
            session_id = f"quiz_{user_id}_{int(time.time())}"
            game_session = GameSession(
                session_id=session_id,
                user_id=user_id,
                game_type="ai_quiz",
                start_time=datetime.now(),
                end_time=None,
                questions_answered=0,
                correct_answers=0,
                score=0,
                time_taken=0.0
            )
            
            self.game_sessions[session_id] = game_session
            
            # Pripremi pitanja za igru
            quiz_questions = []
            for question in selected_questions:
                # Pomešaj odgovore
                all_answers = [question.correct_answer] + question.wrong_answers
                random.shuffle(all_answers)
                
                quiz_questions.append({
                    'id': question.id,
                    'question': question.question,
                    'answers': all_answers,
                    'points': question.points,
                    'difficulty': question.difficulty,
                    'category': question.category
                })
            
            result = {
                'session_id': session_id,
                'game_type': 'ai_quiz',
                'total_questions': question_count,
                'questions': quiz_questions,
                'instructions': "Odgovorite na sva pitanja. Svaki tačan odgovor donosi poene!"
            }
            
            logger.info(f"🎮 AI Quiz pokrenut: {user_id} - {question_count} pitanja")
            return result
            
        except Exception as e:
            logger.error(f"❌ Greška pri pokretanju AI Quiz-a: {e}")
            return {"error": str(e)}
    
    def submit_quiz_answer(self, session_id: str, question_id: str, 
                          selected_answer: str) -> Dict[str, Any]:
        """Predaje odgovor na quiz pitanje"""
        try:
            if session_id not in self.game_sessions:
                return {"error": "Sesija nije pronađena"}
            
            game_session = self.game_sessions[session_id]
            if game_session.end_time:
                return {"error": "Sesija je već završena"}
            
            # Pronađi pitanje
            if question_id not in self.questions:
                return {"error": "Pitanje nije pronađeno"}
            
            question = self.questions[question_id]
            game_session.questions_answered += 1
            
            # Proveri odgovor
            is_correct = selected_answer == question.correct_answer
            if is_correct:
                game_session.correct_answers += 1
                game_session.score += question.points
            
            result = {
                'correct': is_correct,
                'correct_answer': question.correct_answer,
                'explanation': question.explanation,
                'points_earned': question.points if is_correct else 0,
                'current_score': game_session.score,
                'questions_answered': game_session.questions_answered
            }
            
            logger.info(f"✅ Quiz odgovor: {session_id} - {'tačan' if is_correct else 'netačan'}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Greška pri predaji quiz odgovora: {e}")
            return {"error": str(e)}
    
    def finish_quiz(self, session_id: str) -> Dict[str, Any]:
        """Završava quiz sesiju"""
        try:
            if session_id not in self.game_sessions:
                return {"error": "Sesija nije pronađena"}
            
            game_session = self.game_sessions[session_id]
            if game_session.end_time:
                return {"error": "Sesija je već završena"}
            
            # Završi sesiju
            game_session.end_time = datetime.now()
            game_session.time_taken = (game_session.end_time - game_session.start_time).total_seconds()
            
            # Izračunaj rezultat
            accuracy = (game_session.correct_answers / game_session.questions_answered) * 100 if game_session.questions_answered > 0 else 0
            
            # Ažuriraj user progress
            self._update_user_progress(game_session)
            
            # Kreiraj achievements
            achievements = self._check_achievements(game_session)
            
            result = {
                'final_score': game_session.score,
                'questions_answered': game_session.questions_answered,
                'correct_answers': game_session.correct_answers,
                'accuracy': round(accuracy, 1),
                'time_taken': round(game_session.time_taken, 1),
                'achievements': achievements,
                'performance_rating': self._get_performance_rating(accuracy, game_session.score)
            }
            
            logger.info(f"🏁 Quiz završen: {session_id} - Score: {game_session.score}, Accuracy: {accuracy:.1f}%")
            return result
            
        except Exception as e:
            logger.error(f"❌ Greška pri završavanju quiz-a: {e}")
            return {"error": str(e)}
    
    def _update_user_progress(self, game_session: GameSession):
        """Ažurira napredak korisnika"""
        try:
            progress_key = f"{game_session.user_id}_{game_session.game_type}"
            
            if progress_key in self.user_progress:
                progress = self.user_progress[progress_key]
                progress.total_score += game_session.score
                progress.questions_answered += game_session.questions_answered
                progress.correct_answers += game_session.correct_answers
                progress.last_played = datetime.now()
                
                # Ažuriraj streak
                if game_session.correct_answers == game_session.questions_answered:
                    progress.streak += 1
                    progress.best_streak = max(progress.best_streak, progress.streak)
                else:
                    progress.streak = 0
            else:
                # Kreiraj novi progress
                progress = UserProgress(
                    user_id=game_session.user_id,
                    game_type=game_session.game_type,
                    total_score=game_session.score,
                    questions_answered=game_session.questions_answered,
                    correct_answers=game_session.correct_answers,
                    streak=1 if game_session.correct_answers == game_session.questions_answered else 0,
                    best_streak=1 if game_session.correct_answers == game_session.questions_answered else 0,
                    last_played=datetime.now(),
                    achievements=[]
                )
                self.user_progress[progress_key] = progress
            
            self._save_games_data()
            
        except Exception as e:
            logger.error(f"❌ Greška pri ažuriranju user progress-a: {e}")
    
    def _check_achievements(self, game_session: GameSession) -> List[str]:
        """Proverava achievements"""
        try:
            achievements = []
            
            # Perfect Score achievement
            if game_session.correct_answers == game_session.questions_answered:
                achievements.append("🏆 Perfect Score - 100% tačnost!")
            
            # High Score achievement
            if game_session.score >= 100:
                achievements.append("⭐ High Scorer - 100+ poena!")
            
            # Speed achievement
            if game_session.time_taken < 300:  # Manje od 5 minuta
                achievements.append("⚡ Speed Demon - Brzo završeno!")
            
            # Streak achievement
            if game_session.correct_answers >= 5:
                achievements.append("🔥 Hot Streak - 5+ tačnih odgovora!")
            
            return achievements
            
        except Exception as e:
            logger.error(f"❌ Greška pri proveri achievements: {e}")
            return []
    
    def _get_performance_rating(self, accuracy: float, score: int) -> str:
        """Vraća performance rating"""
        if accuracy >= 90 and score >= 80:
            return "🌟 Excellent"
        elif accuracy >= 80 and score >= 60:
            return "⭐ Very Good"
        elif accuracy >= 70 and score >= 40:
            return "👍 Good"
        elif accuracy >= 60 and score >= 20:
            return "😊 Fair"
        else:
            return "📚 Keep Learning"
    
    def ai_learning_challenge(self, user_id: str = "default", challenge_type: str = "daily") -> Dict[str, Any]:
        """Pokreće AI Learning Challenge"""
        try:
            if challenge_type == "daily":
                # Dnevni challenge - 5 teških pitanja
                challenge_questions = [
                    q for q in self.questions.values() 
                    if q.difficulty == "hard"
                ][:5]
                challenge_name = "Daily AI Challenge"
                bonus_points = 50
            elif challenge_type == "weekly":
                # Nedeljni challenge - 10 pitanja različitih težina
                challenge_questions = random.sample(list(self.questions.values()), 10)
                challenge_name = "Weekly AI Challenge"
                bonus_points = 100
            else:
                return {"error": "Nepoznat tip challenge-a"}
            
            if len(challenge_questions) < 3:
                return {"error": "Nema dovoljno pitanja za challenge"}
            
            # Kreiraj challenge session
            session_id = f"challenge_{challenge_type}_{user_id}_{int(time.time())}"
            challenge_session = GameSession(
                session_id=session_id,
                user_id=user_id,
                game_type=f"ai_challenge_{challenge_type}",
                start_time=datetime.now(),
                end_time=None,
                questions_answered=0,
                correct_answers=0,
                score=0,
                time_taken=0.0
            )
            
            self.game_sessions[session_id] = challenge_session
            
            # Pripremi challenge
            challenge_data = []
            for question in challenge_questions:
                all_answers = [question.correct_answer] + question.wrong_answers
                random.shuffle(all_answers)
                
                challenge_data.append({
                    'id': question.id,
                    'question': question.question,
                    'answers': all_answers,
                    'points': question.points * 2,  # Dupli poeni za challenge
                    'difficulty': question.difficulty,
                    'category': question.category
                })
            
            result = {
                'session_id': session_id,
                'challenge_name': challenge_name,
                'challenge_type': challenge_type,
                'total_questions': len(challenge_questions),
                'questions': challenge_data,
                'bonus_points': bonus_points,
                'instructions': f"Završite {challenge_name} za bonus poene! Dupli poeni za svaki tačan odgovor."
            }
            
            logger.info(f"🎯 AI Learning Challenge pokrenut: {challenge_type} - {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Greška pri pokretanju AI Learning Challenge: {e}")
            return {"error": str(e)}
    
    def get_user_stats(self, user_id: str = "default") -> Dict[str, Any]:
        """Vraća statistiku korisnika"""
        try:
            user_stats = {
                'user_id': user_id,
                'total_games_played': 0,
                'total_score': 0,
                'best_score': 0,
                'average_accuracy': 0.0,
                'total_questions': 0,
                'correct_answers': 0,
                'achievements': [],
                'game_types': {}
            }
            
            # Prikuplji podatke iz svih game types
            for progress_key, progress in self.user_progress.items():
                if progress.user_id == user_id:
                    user_stats['total_games_played'] += 1
                    user_stats['total_score'] += progress.total_score
                    user_stats['total_questions'] += progress.questions_answered
                    user_stats['correct_answers'] += progress.correct_answers
                    user_stats['achievements'].extend(progress.achievements)
                    
                    # Game type specific stats
                    if progress.game_type not in user_stats['game_types']:
                        user_stats['game_types'][progress.game_type] = {
                            'games_played': 0,
                            'total_score': 0,
                            'best_streak': 0
                        }
                    
                    user_stats['game_types'][progress.game_type]['games_played'] += 1
                    user_stats['game_types'][progress.game_type]['total_score'] += progress.total_score
                    user_stats['game_types'][progress.game_type]['best_streak'] = max(
                        user_stats['game_types'][progress.game_type]['best_streak'],
                        progress.best_streak
                    )
            
            # Izračunaj proseke
            if user_stats['total_questions'] > 0:
                user_stats['average_accuracy'] = (user_stats['correct_answers'] / user_stats['total_questions']) * 100
            
            # Ukloni duplikate achievements
            user_stats['achievements'] = list(set(user_stats['achievements']))
            
            return user_stats
            
        except Exception as e:
            logger.error(f"❌ Greška pri dohvatanju user stats: {e}")
            return {"error": str(e)}
    
    def get_leaderboard(self, game_type: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Vraća leaderboard"""
        try:
            leaderboard = []
            
            for progress_key, progress in self.user_progress.items():
                if game_type is None or progress.game_type == game_type:
                    leaderboard.append({
                        'user_id': progress.user_id,
                        'game_type': progress.game_type,
                        'total_score': progress.total_score,
                        'questions_answered': progress.questions_answered,
                        'correct_answers': progress.correct_answers,
                        'accuracy': (progress.correct_answers / progress.questions_answered * 100) if progress.questions_answered > 0 else 0,
                        'best_streak': progress.best_streak,
                        'last_played': progress.last_played.isoformat()
                    })
            
            # Sortiraj po score-u
            leaderboard.sort(key=lambda x: x['total_score'], reverse=True)
            
            return leaderboard[:limit]
            
        except Exception as e:
            logger.error(f"❌ Greška pri dohvatanju leaderboard-a: {e}")
            return []
    
    def add_custom_question(self, question: GameQuestion) -> bool:
        """Dodaje custom pitanje"""
        try:
            if question.id in self.questions:
                logger.warning(f"⚠️ Pitanje sa ID {question.id} već postoji")
                return False
            
            self.questions[question.id] = question
            self._save_games_data()
            
            logger.info(f"✅ Custom pitanje dodato: {question.id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Greška pri dodavanju custom pitanja: {e}")
            return False
    
    def clear_user_data(self, user_id: str):
        """Briše podatke korisnika"""
        try:
            # Obriši user progress
            keys_to_remove = [key for key in self.user_progress.keys() if key.startswith(f"{user_id}_")]
            for key in keys_to_remove:
                del self.user_progress[key]
            
            # Obriši game sessions
            sessions_to_remove = [sess_id for sess_id, sess in self.game_sessions.items() if sess.user_id == user_id]
            for sess_id in sessions_to_remove:
                del self.game_sessions[sess_id]
            
            self._save_games_data()
            logger.info(f"🧹 User data obrisan za: {user_id}")
            
        except Exception as e:
            logger.error(f"❌ Greška pri brisanju user data: {e}")

# Globalna instanca
interactive_learning_games = None

def get_interactive_learning_games() -> InteractiveLearningGames:
    """Vraća globalnu instancu Interactive Learning Games-a"""
    global interactive_learning_games
    if interactive_learning_games is None:
        interactive_learning_games = InteractiveLearningGames()
    return interactive_learning_games
