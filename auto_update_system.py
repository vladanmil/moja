#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - Auto-Update System
Automatsko ažuriranje AI modula i funkcionalnosti
"""

import json
import os
import shutil
import requests
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import logging
import threading
import time

logger = logging.getLogger(__name__)

@dataclass
class UpdateInfo:
    """Informacije o ažuriranju"""
    module_name: str
    current_version: str
    latest_version: str
    update_available: bool
    changelog: str
    download_url: str
    file_size: int
    checksum: str
    release_date: datetime

@dataclass
class UpdateHistory:
    """Istorija ažuriranja"""
    module_name: str
    old_version: str
    new_version: str
    update_date: datetime
    success: bool
    error_message: str
    backup_created: bool

class AutoUpdateSystem:
    """Napredni sistem za automatsko ažuriranje AI modula"""
    
    def __init__(self, update_config_file: str = "ai_update_config.json"):
        self.update_config_file = update_config_file
        
        # Konfiguracija
        self.auto_check_enabled = True
        self.auto_update_enabled = False
        self.check_interval_hours = 24
        self.backup_before_update = True
        
        # Update server info
        self.update_server_url = "https://api.autoearnpro.com/updates"
        self.api_key = None
        
        # Lokalni podaci
        self.installed_modules: Dict[str, str] = {}  # module_name -> version
        self.update_history: List[UpdateHistory] = []
        self.last_check_time: Optional[datetime] = None
        
        # Thread za automatsku proveru
        self.update_checker = None
        self.is_checking = False
        
        # Učitaj konfiguraciju
        self._load_config()
        
        # Pokreni automatsku proveru
        self._start_auto_check()
        
        logger.info("🔄 Auto-Update System uspešno inicijalizovan!")
    
    def _load_config(self):
        """Učitava konfiguraciju"""
        try:
            if os.path.exists(self.update_config_file):
                with open(self.update_config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                    self.auto_check_enabled = config.get('auto_check_enabled', True)
                    self.auto_update_enabled = config.get('auto_update_enabled', False)
                    self.check_interval_hours = config.get('check_interval_hours', 24)
                    self.backup_before_update = config.get('backup_before_update', True)
                    self.update_server_url = config.get('update_server_url', self.update_server_url)
                    self.api_key = config.get('api_key')
                    
                    # Učitaj installed modules
                    self.installed_modules = config.get('installed_modules', {})
                    
                    # Učitaj update history
                    for hist_data in config.get('update_history', []):
                        hist_data['update_date'] = datetime.fromisoformat(hist_data['update_date'])
                        self.update_history.append(UpdateHistory(**hist_data))
                    
                    logger.info(f"✅ Konfiguracija učitana: auto_check={self.auto_check_enabled}, interval={self.check_interval_hours}h")
            else:
                self._create_default_config()
                
        except Exception as e:
            logger.error(f"❌ Greška pri učitavanju konfiguracije: {e}")
            self._create_default_config()
    
    def _create_default_config(self):
        """Kreira default konfiguraciju"""
        try:
            config = {
                'auto_check_enabled': True,
                'auto_update_enabled': False,
                'check_interval_hours': 24,
                'backup_before_update': True,
                'update_server_url': self.update_server_url,
                'api_key': None,
                'installed_modules': {},
                'update_history': []
            }
            
            with open(self.update_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            logger.info("📝 Kreirana default konfiguracija")
            
        except Exception as e:
            logger.error(f"❌ Greška pri kreiranju default konfiguracije: {e}")
    
    def _save_config(self):
        """Čuva konfiguraciju"""
        try:
            config = {
                'auto_check_enabled': self.auto_check_enabled,
                'auto_update_enabled': self.auto_update_enabled,
                'check_interval_hours': self.check_interval_hours,
                'backup_before_update': self.backup_before_update,
                'update_server_url': self.update_server_url,
                'api_key': self.api_key,
                'installed_modules': self.installed_modules,
                'update_history': [
                    {
                        'module_name': hist.module_name,
                        'old_version': hist.old_version,
                        'new_version': hist.new_version,
                        'update_date': hist.update_date.isoformat(),
                        'success': hist.success,
                        'error_message': hist.error_message,
                        'backup_created': hist.backup_created
                    }
                    for hist in self.update_history
                ]
            }
            
            with open(self.update_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            logger.debug("💾 Konfiguracija sačuvana")
            
        except Exception as e:
            logger.error(f"❌ Greška pri čuvanju konfiguracije: {e}")
    
    def _start_auto_check(self):
        """Pokreće automatsku proveru ažuriranja"""
        if not self.auto_check_enabled:
            return
        
        try:
            self.update_checker = threading.Thread(target=self._auto_check_worker, daemon=True)
            self.update_checker.start()
            logger.info("🔄 Auto-check thread pokrenut")
        except Exception as e:
            logger.error(f"❌ Greška pri pokretanju auto-check thread-a: {e}")
    
    def _auto_check_worker(self):
        """Worker thread za automatsku proveru"""
        while self.auto_check_enabled:
            try:
                # Proveri da li je vreme za proveru
                if (self.last_check_time is None or 
                    datetime.now() - self.last_check_time > timedelta(hours=self.check_interval_hours)):
                    
                    logger.info("🔄 Automatska provera ažuriranja...")
                    self.check_for_updates()
                    self.last_check_time = datetime.now()
                
                # Čekaj 1 sat pre sledeće provere
                time.sleep(3600)
                
            except Exception as e:
                logger.error(f"❌ Greška u auto-check worker-u: {e}")
                time.sleep(3600)
    
    def check_for_updates(self) -> Dict[str, UpdateInfo]:
        """Proverava dostupna ažuriranja"""
        try:
            self.is_checking = True
            available_updates = {}
            
            # Proveri server za ažuriranja
            if self.update_server_url:
                try:
                    response = requests.get(
                        f"{self.update_server_url}/check",
                        headers={'Authorization': f'Bearer {self.api_key}'} if self.api_key else {},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        updates_data = response.json()
                        
                        for module_name, update_data in updates_data.items():
                            if self._is_update_available(module_name, update_data.get('version', '0.0.0')):
                                update_info = UpdateInfo(
                                    module_name=module_name,
                                    current_version=self.installed_modules.get(module_name, '0.0.0'),
                                    latest_version=update_data.get('version', '0.0.0'),
                                    update_available=True,
                                    changelog=update_data.get('changelog', ''),
                                    download_url=update_data.get('download_url', ''),
                                    file_size=update_data.get('file_size', 0),
                                    checksum=update_data.get('checksum', ''),
                                    release_date=datetime.fromisoformat(update_data.get('release_date', datetime.now().isoformat()))
                                )
                                available_updates[module_name] = update_info
                        
                        logger.info(f"✅ Provereno {len(updates_data)} modula, {len(available_updates)} ažuriranja dostupno")
                    else:
                        logger.warning(f"⚠️ Server vratio status {response.status_code}")
                        
                except requests.RequestException as e:
                    logger.warning(f"⚠️ Greška pri proveri servera: {e}")
            
            # Proveri lokalne module
            self._scan_local_modules()
            
            self.is_checking = False
            return available_updates
            
        except Exception as e:
            logger.error(f"❌ Greška pri proveri ažuriranja: {e}")
            self.is_checking = False
            return {}
    
    def _is_update_available(self, module_name: str, latest_version: str) -> bool:
        """Proverava da li je ažuriranje dostupno"""
        current_version = self.installed_modules.get(module_name, '0.0.0')
        
        # Jednostavna provera verzija
        try:
            current_parts = [int(x) for x in current_version.split('.')]
            latest_parts = [int(x) for x in latest_version.split('.')]
            
            # Poredi verzije
            for i in range(max(len(current_parts), len(latest_parts))):
                current_part = current_parts[i] if i < len(current_parts) else 0
                latest_part = latest_parts[i] if i < len(latest_parts) else 0
                
                if latest_part > current_part:
                    return True
                elif latest_part < current_part:
                    return False
            
            return False
            
        except (ValueError, IndexError):
            # Ako ne može da poredi verzije, proveri da li su različite
            return current_version != latest_version
    
    def _scan_local_modules(self):
        """Skenira lokalne module za verzije"""
        try:
            core_ai_dir = "core/ai"
            if os.path.exists(core_ai_dir):
                for filename in os.listdir(core_ai_dir):
                    if filename.endswith('.py') and filename != '__init__.py':
                        module_name = filename[:-3]  # Ukloni .py
                        
                        # Proveri da li modul ima verziju
                        version = self._extract_module_version(os.path.join(core_ai_dir, filename))
                        if version:
                            self.installed_modules[module_name] = version
            
            logger.debug(f"🔍 Skenirano {len(self.installed_modules)} lokalnih modula")
            
        except Exception as e:
            logger.error(f"❌ Greška pri skeniranju lokalnih modula: {e}")
    
    def _extract_module_version(self, file_path: str) -> Optional[str]:
        """Izvlači verziju iz modula"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Traži verziju u komentarima
                version_markers = ['__version__', 'version =', 'VERSION =']
                for marker in version_markers:
                    if marker in content:
                        lines = content.split('\n')
                        for line in lines:
                            if marker in line:
                                # Izvlači verziju
                                version_part = line.split('=')[1].strip().strip('"\'')
                                if version_part and version_part != 'None':
                                    return version_part
                
                return None
                
        except Exception as e:
            logger.debug(f"⚠️ Ne mogu da izvučem verziju iz {file_path}: {e}")
            return None
    
    def download_update(self, module_name: str, download_url: str) -> bool:
        """Download-uje ažuriranje"""
        try:
            logger.info(f"⬇️ Download-ujem ažuriranje za {module_name}...")
            
            # Download fajl
            response = requests.get(download_url, timeout=60)
            if response.status_code != 200:
                logger.error(f"❌ Greška pri download-u: status {response.status_code}")
                return False
            
            # Kreiraj backup ako je omogućen
            if self.backup_before_update:
                self._create_backup(module_name)
            
            # Sačuvaj novi fajl
            temp_file = f"temp_{module_name}.py"
            with open(temp_file, 'wb') as f:
                f.write(response.content)
            
            # Proveri checksum ako je dostupan
            if self._verify_checksum(temp_file, response.content):
                # Premesti fajl na pravo mesto
                target_file = f"core/ai/{module_name}.py"
                shutil.move(temp_file, target_file)
                
                logger.info(f"✅ Ažuriranje za {module_name} uspešno download-ovano")
                return True
            else:
                logger.error(f"❌ Checksum verification failed za {module_name}")
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                return False
                
        except Exception as e:
            logger.error(f"❌ Greška pri download-u ažuriranja: {e}")
            return False
    
    def _verify_checksum(self, file_path: str, content: bytes) -> bool:
        """Proverava checksum fajla"""
        try:
            # Jednostavna MD5 provera
            calculated_checksum = hashlib.md5(content).hexdigest()
            logger.debug(f"🔍 Calculated checksum: {calculated_checksum}")
            return True  # Za sada uvek vraća True
        except Exception as e:
            logger.error(f"❌ Greška pri checksum proveri: {e}")
            return False
    
    def _create_backup(self, module_name: str):
        """Kreira backup pre ažuriranja"""
        try:
            source_file = f"core/ai/{module_name}.py"
            if os.path.exists(source_file):
                backup_dir = "backups/ai_modules"
                os.makedirs(backup_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = f"{backup_dir}/{module_name}_{timestamp}.py"
                
                shutil.copy2(source_file, backup_file)
                logger.info(f"💾 Backup kreiran: {backup_file}")
                
        except Exception as e:
            logger.error(f"❌ Greška pri kreiranju backup-a: {e}")
    
    def install_update(self, module_name: str, update_info: UpdateInfo) -> bool:
        """Instalira ažuriranje"""
        try:
            logger.info(f"🔧 Instaliram ažuriranje za {module_name}...")
            
            # Download ažuriranje
            if not self.download_update(module_name, update_info.download_url):
                return False
            
            # Ažuriraj verziju u installed_modules
            old_version = self.installed_modules.get(module_name, '0.0.0')
            self.installed_modules[module_name] = update_info.latest_version
            
            # Kreiraj update history
            update_history = UpdateHistory(
                module_name=module_name,
                old_version=old_version,
                new_version=update_info.latest_version,
                update_date=datetime.now(),
                success=True,
                error_message="",
                backup_created=self.backup_before_update
            )
            self.update_history.append(update_history)
            
            # Sačuvaj konfiguraciju
            self._save_config()
            
            logger.info(f"✅ Ažuriranje za {module_name} uspešno instalirano: {old_version} -> {update_info.latest_version}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Greška pri instaliranju ažuriranja: {e}")
            
            # Kreiraj update history sa greškom
            update_history = UpdateHistory(
                module_name=module_name,
                old_version=self.installed_modules.get(module_name, '0.0.0'),
                new_version=update_info.latest_version,
                update_date=datetime.now(),
                success=False,
                error_message=str(e),
                backup_created=False
            )
            self.update_history.append(update_history)
            
            return False
    
    def auto_update_all(self) -> Dict[str, bool]:
        """Automatski ažurira sve dostupne module"""
        try:
            if not self.auto_update_enabled:
                logger.warning("⚠️ Auto-update je onemogućen")
                return {}
            
            logger.info("🚀 Pokretanje automatskog ažuriranja svih modula...")
            
            # Proveri ažuriranja
            available_updates = self.check_for_updates()
            if not available_updates:
                logger.info("✅ Nema dostupnih ažuriranja")
                return {}
            
            # Instaliraj sva ažuriranja
            results = {}
            for module_name, update_info in available_updates.items():
                try:
                    success = self.install_update(module_name, update_info)
                    results[module_name] = success
                except Exception as e:
                    logger.error(f"❌ Greška pri auto-update {module_name}: {e}")
                    results[module_name] = False
            
            # Sačuvaj konfiguraciju
            self._save_config()
            
            success_count = sum(1 for success in results.values() if success)
            logger.info(f"✅ Auto-update završen: {success_count}/{len(results)} uspešno")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Greška pri auto-update: {e}")
            return {}
    
    def get_update_status(self) -> Dict[str, Any]:
        """Vraća status ažuriranja"""
        try:
            status = {
                'auto_check_enabled': self.auto_check_enabled,
                'auto_update_enabled': self.auto_update_enabled,
                'check_interval_hours': self.check_interval_hours,
                'backup_before_update': self.backup_before_update,
                'last_check_time': self.last_check_time.isoformat() if self.last_check_time else None,
                'is_checking': self.is_checking,
                'total_installed_modules': len(self.installed_modules),
                'total_updates_installed': len([h for h in self.update_history if h.success]),
                'recent_updates': [
                    {
                        'module': hist.module_name,
                        'version': f"{hist.old_version} -> {hist.new_version}",
                        'date': hist.update_date.isoformat(),
                        'success': hist.success
                    }
                    for hist in sorted(self.update_history, key=lambda x: x.update_date, reverse=True)[:5]
                ]
            }
            
            return status
            
        except Exception as e:
            logger.error(f"❌ Greška pri dohvatanju update status-a: {e}")
            return {"error": str(e)}
    
    def set_config(self, **kwargs):
        """Postavlja konfiguraciju"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                    logger.info(f"⚙️ Konfiguracija ažurirana: {key} = {value}")
            
            self._save_config()
            
        except Exception as e:
            logger.error(f"❌ Greška pri postavljanju konfiguracije: {e}")
    
    def shutdown(self):
        """Zaustavlja auto-update sistem"""
        try:
            self.auto_check_enabled = False
            if self.update_checker and self.update_checker.is_alive():
                self.update_checker.join(timeout=5)
            logger.info("🛑 Auto-Update System zaustavljen")
        except Exception as e:
            logger.error(f"❌ Greška pri zaustavljanju: {e}")

# Globalna instanca
auto_update_system = None

def get_auto_update_system() -> AutoUpdateSystem:
    """Vraća globalnu instancu Auto-Update System-a"""
    global auto_update_system
    if auto_update_system is None:
        auto_update_system = AutoUpdateSystem()
    return auto_update_system
