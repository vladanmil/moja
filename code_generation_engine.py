#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoEarnPro - Code Generation Engine
AI asistent može da kodira, kreira GUI prozore i generiše kod
"""

import json
import os
import re
import ast
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class CodeTemplate:
    """Template za generisanje koda"""
    id: str
    name: str
    description: str
    category: str
    template_code: str
    parameters: List[str]
    examples: List[str]
    tags: List[str]

@dataclass
class GeneratedCode:
    """Generisani kod"""
    id: str
    template_id: str
    generated_code: str
    parameters_used: Dict[str, Any]
    timestamp: datetime
    user_request: str
    code_type: str
    file_path: str

@dataclass
class CodeAnalysis:
    """Analiza koda"""
    code_id: str
    syntax_valid: bool
    complexity_score: float
    line_count: int
    function_count: int
    class_count: int
    suggestions: List[str]
    errors: List[str]

class CodeGenerationEngine:
    """Napredni engine za generisanje koda i GUI prozora"""
    
    def __init__(self, templates_file: str = "code_templates.json"):
        self.templates_file = templates_file
        
        # Glavni podaci
        self.code_templates: Dict[str, CodeTemplate] = {}
        self.generated_codes: Dict[str, GeneratedCode] = {}
        self.code_analyses: Dict[str, CodeAnalysis] = {}
        
        # Učitaj postojeće template-e
        self._load_templates()
        
        # Kreiraj default template-e ako ne postoje
        if not self.code_templates:
            self._create_default_templates()
        
        logger.info("🛠️ Code Generation Engine uspešno inicijalizovan!")
    
    def _load_templates(self):
        """Učitava postojeće code template-e"""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Učitaj code templates
                    for template_data in data.get('code_templates', []):
                        self.code_templates[template_data['id']] = CodeTemplate(**template_data)
                    
                    # Učitaj generated codes
                    for code_data in data.get('generated_codes', []):
                        code_data['timestamp'] = datetime.fromisoformat(code_data['timestamp'])
                        self.generated_codes[code_data['id']] = GeneratedCode(**code_data)
                    
                    logger.info(f"✅ Učitano {len(self.code_templates)} code template-a i {len(self.generated_codes)} generisanih kodova")
                    
        except FileNotFoundError:
            logger.info("📝 Kreiran novi templates fajl")
        except Exception as e:
            logger.error(f"❌ Greška pri učitavanju templates: {e}")
    
    def _save_templates(self):
        """Čuva code template-e"""
        try:
            data = {
                'code_templates': [asdict(template) for template in self.code_templates.values()],
                'generated_codes': [
                    {
                        'id': code.id,
                        'template_id': code.template_id,
                        'generated_code': code.generated_code,
                        'parameters_used': code.parameters_used,
                        'timestamp': code.timestamp.isoformat(),
                        'user_request': code.user_request,
                        'code_type': code.code_type,
                        'file_path': code.file_path
                    }
                    for code in self.generated_codes.values()
                ]
            }
            
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.debug("💾 Templates sačuvani")
            
        except Exception as e:
            logger.error(f"❌ Greška pri čuvanju templates: {e}")
    
    def _create_default_templates(self):
        """Kreira default code template-e"""
        try:
            default_templates = [
                # GUI Window Template
                CodeTemplate(
                    id="gui_window",
                    name="GUI Window Generator",
                    description="Kreira Tkinter GUI prozor sa osnovnim funkcionalnostima",
                    category="gui",
                    template_code="""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
{window_name} - {description}
\"\"\"

import tkinter as tk
from tkinter import ttk, messagebox
import json
import logging

logger = logging.getLogger(__name__)

class {class_name}(tk.Toplevel):
    \"\"\"{window_name} prozor\"\"\"
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Konfiguracija prozora
        self.title("{window_name}")
        self.geometry("{window_size}")
        self.resizable(True, True)
        
        # Centriraj prozor
        self.center_window()
        
        # Inicijalizacija
        self._init_ui()
        self._init_data()
        
        logger.info(f"✅ {window_name} prozor uspešno otvoren")
    
    def center_window(self):
        \"\"\"Centrira prozor na ekranu\"\"\"
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def _init_ui(self):
        \"\"\"Inicijalizuje korisnički interfejs\"\"\"
        # Glavni frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Naslov
        title_label = ttk.Label(main_frame, text="{window_name}", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # {ui_elements}
        
        # Kontrole
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=20)
        
        # Dugmad
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(button_frame, text="Zatvori", command=self.close_window).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Sačuvaj", command=self.save_data).pack(side=tk.RIGHT, padx=5)
    
    def _init_data(self):
        \"\"\"Inicijalizuje podatke\"\"\"
        # TODO: Implementiraj učitavanje podataka
        pass
    
    def save_data(self):
        \"\"\"Čuva podatke\"\"\"
        try:
            # TODO: Implementiraj čuvanje podataka
            messagebox.showinfo("Uspeh", "Podaci uspešno sačuvani!")
            logger.info("💾 Podaci sačuvani")
        except Exception as e:
            messagebox.showerror("Greška", f"Greška pri čuvanju: {e}")
            logger.error(f"❌ Greška pri čuvanju: {e}")
    
    def close_window(self):
        \"\"\"Zatvara prozor\"\"\"
        self.destroy()
        logger.info(f"🛑 {window_name} prozor zatvoren")

# Test funkcija
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Sakrij glavni prozor
    
    app = {class_name}(root)
    root.mainloop()
""",
                    parameters=["window_name", "description", "class_name", "window_size", "ui_elements"],
                    examples=[
                        "Kreiraj GUI prozor za upravljanje korisnicima",
                        "Napravi prozor za konfiguraciju sistema",
                        "Generiši GUI za analizu podataka"
                    ],
                    tags=["gui", "tkinter", "window", "interface"]
                ),
                
                # Data Processing Template
                CodeTemplate(
                    id="data_processor",
                    name="Data Processing Script",
                    description="Kreira Python skriptu za obradu podataka",
                    category="data_processing",
                    template_code="""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
{script_name} - {description}
\"\"\"

import pandas as pd
import numpy as np
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import seaborn as sns

# Konfiguracija logging-a
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class {class_name}:
    \"\"\"{description}\"\"\"
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file
        self.data = None
        self.processed_data = None
        self.results = {}
        
        # Učitaj konfiguraciju
        self._load_config()
        
        logger.info(f"✅ {class_name} uspešno inicijalizovan")
    
    def _load_config(self):
        \"\"\"Učitava konfiguraciju\"\"\"
        try:
            if self.config_file and os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                logger.info("✅ Konfiguracija učitana")
            else:
                self.config = self._get_default_config()
                logger.info("📝 Korišćena default konfiguracija")
        except Exception as e:
            logger.error(f"❌ Greška pri učitavanju konfiguracije: {e}")
            self.config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        \"\"\"Vraća default konfiguraciju\"\"\"
        return {
            'input_file': 'data/input.csv',
            'output_file': 'data/output.csv',
            'delimiter': ',',
            'encoding': 'utf-8',
            'process_columns': [],
            'filters': {},
            'aggregations': []
        }
    
    def load_data(self, file_path: str = None) -> bool:
        \"\"\"Učitava podatke\"\"\"
        try:
            file_path = file_path or self.config.get('input_file')
            
            if file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path, delimiter=self.config.get('delimiter', ','))
            elif file_path.endswith('.json'):
                self.data = pd.read_json(file_path)
            elif file_path.endswith('.xlsx'):
                self.data = pd.read_excel(file_path)
            else:
                logger.error(f"❌ Nepodržan format fajla: {file_path}")
                return False
            
            logger.info(f"✅ Podaci učitani: {len(self.data)} redova, {len(self.data.columns)} kolona")
            return True
            
        except Exception as e:
            logger.error(f"❌ Greška pri učitavanju podataka: {e}")
            return False
    
    def process_data(self) -> bool:
        \"\"\"Obrađuje podatke\"\"\"
        try:
            if self.data is None:
                logger.error("❌ Nema podataka za obradu")
                return False
            
            # Kopiraj podatke
            self.processed_data = self.data.copy()
            
            # Primeni filtere
            self._apply_filters()
            
            # Primeni transformacije
            self._apply_transformations()
            
            # Primeni agregacije
            self._apply_aggregations()
            
            logger.info("✅ Podaci uspešno obrađeni")
            return True
            
        except Exception as e:
            logger.error(f"❌ Greška pri obradi podataka: {e}")
            return False
    
    def _apply_filters(self):
        \"\"\"Primenjuje filtere\"\"\"
        filters = self.config.get('filters', {})
        
        for column, filter_config in filters.items():
            if column in self.processed_data.columns:
                if filter_config.get('type') == 'range':
                    min_val = filter_config.get('min')
                    max_val = filter_config.get('max')
                    if min_val is not None:
                        self.processed_data = self.processed_data[self.processed_data[column] >= min_val]
                    if max_val is not None:
                        self.processed_data = self.processed_data[self.processed_data[column] <= max_val]
                elif filter_config.get('type') == 'values':
                    values = filter_config.get('values', [])
                    if values:
                        self.processed_data = self.processed_data[self.processed_data[column].isin(values)]
    
    def _apply_transformations(self):
        \"\"\"Primenjuje transformacije\"\"\"
        # TODO: Implementiraj specifične transformacije
        pass
    
    def _apply_aggregations(self):
        \"\"\"Primenjuje agregacije\"\"\"
        aggregations = self.config.get('aggregations', [])
        
        if aggregations and self.processed_data is not None:
            agg_results = self.processed_data.groupby(aggregations.get('group_by', [])).agg(aggregations.get('functions', {}))
            self.results['aggregations'] = agg_results
    
    def save_results(self, output_file: str = None) -> bool:
        \"\"\"Čuva rezultate\"\"\"
        try:
            output_file = output_file or self.config.get('output_file')
            
            if self.processed_data is not None:
                if output_file.endswith('.csv'):
                    self.processed_data.to_csv(output_file, index=False)
                elif output_file.endswith('.json'):
                    self.processed_data.to_json(output_file, orient='records', indent=2)
                elif output_file.endswith('.xlsx'):
                    self.processed_data.to_excel(output_file, index=False)
                
                logger.info(f"✅ Rezultati sačuvani u {output_file}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Greška pri čuvanju rezultata: {e}")
            return False
    
    def generate_report(self) -> str:
        \"\"\"Generiše izveštaj\"\"\"
        try:
            if self.processed_data is None:
                return "Nema podataka za izveštaj"
            
            report = f\"\"\"
# Izveštaj obrade podataka
**Generisan:** {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}

## Statistike
- **Ukupno redova:** {{len(self.processed_data)}}
- **Ukupno kolona:** {{len(self.processed_data.columns)}}
- **Tipovi podataka:**
\"\"\"
            
            for col, dtype in self.processed_data.dtypes.items():
                report += f"  - {{col}}: {{dtype}}\\n"
            
            report += f\"\"\"
## Numeričke kolone
\"\"\"
            
            numeric_cols = self.processed_data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                stats = self.processed_data[col].describe()
                report += f"**{{col}}:**\\n"
                report += f"  - Min: {{stats['min']:.2f}}\\n"
                report += f"  - Max: {{stats['max']:.2f}}\\n"
                report += f"  - Mean: {{stats['mean']:.2f}}\\n"
                report += f"  - Std: {{stats['std']:.2f}}\\n\\n"
            
            return report
            
        except Exception as e:
            logger.error(f"❌ Greška pri generisanju izveštaja: {e}")
            return f"Greška pri generisanju izveštaja: {e}"

def main():
    \"\"\"Glavna funkcija\"\"\"
    try:
        # Inicijalizuj processor
        processor = {class_name}()
        
        # Učitaj podatke
        if not processor.load_data():
            logger.error("❌ Ne mogu da učitam podatke")
            return
        
        # Obradi podatke
        if not processor.process_data():
            logger.error("❌ Greška pri obradi podataka")
            return
        
        # Sačuvaj rezultate
        if not processor.save_results():
            logger.error("❌ Greška pri čuvanju rezultata")
            return
        
        # Generiši izveštaj
        report = processor.generate_report()
        print(report)
        
        logger.info("✅ Obrada podataka uspešno završena")
        
    except Exception as e:
        logger.error(f"❌ Greška u main funkciji: {e}")

if __name__ == "__main__":
    main()
""",
                    parameters=["script_name", "description", "class_name"],
                    examples=[
                        "Kreiraj skriptu za analizu CSV podataka",
                        "Napravi data processor za JSON fajlove",
                        "Generiši skriptu za agregaciju podataka"
                    ],
                    tags=["data", "pandas", "processing", "analysis"]
                )
            ]
            
            for template in default_templates:
                self.code_templates[template.id] = template
            
            logger.info(f"✅ Kreirano {len(default_templates)} default template-a")
            self._save_templates()
            
        except Exception as e:
            logger.error(f"❌ Greška pri kreiranju default template-a: {e}")
    
    def generate_code(self, template_id: str, parameters: Dict[str, Any], 
                      user_request: str = "") -> Optional[GeneratedCode]:
        """Generiše kod na osnovu template-a i parametara"""
        try:
            if template_id not in self.code_templates:
                logger.error(f"❌ Template {template_id} nije pronađen")
                return None
            
            template = self.code_templates[template_id]
            
            # Proveri da li su svi obavezni parametri prisutni
            missing_params = [param for param in template.parameters if param not in parameters]
            if missing_params:
                logger.error(f"❌ Nedostaju parametri: {missing_params}")
                return None
            
            # Generiši kod
            generated_code = template.template_code
            for param, value in parameters.items():
                generated_code = generated_code.replace(f"{{{param}}}", str(value))
            
            # Kreiraj generated code objekat
            code_id = f"code_{template_id}_{int(datetime.now().timestamp())}"
            generated_code_obj = GeneratedCode(
                id=code_id,
                template_id=template_id,
                generated_code=generated_code,
                parameters_used=parameters,
                timestamp=datetime.now(),
                user_request=user_request,
                code_type=template.category,
                file_path=""
            )
            
            self.generated_codes[code_id] = generated_code_obj
            
            logger.info(f"✅ Kod generisan: {template_id} - {code_id}")
            return generated_code_obj
            
        except Exception as e:
            logger.error(f"❌ Greška pri generisanju koda: {e}")
            return None
    
    def save_generated_code(self, code_id: str, file_path: str) -> bool:
        """Čuva generisani kod u fajl"""
        try:
            if code_id not in self.generated_codes:
                logger.error(f"❌ Generisani kod {code_id} nije pronađen")
                return False
            
            generated_code = self.generated_codes[code_id]
            
            # Kreiraj direktorijum ako ne postoji
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Sačuvaj kod
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(generated_code.generated_code)
            
            # Ažuriraj file_path
            generated_code.file_path = file_path
            self._save_templates()
            
            logger.info(f"✅ Kod sačuvan u {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Greška pri čuvanju koda: {e}")
            return False
    
    def analyze_code(self, code_id: str) -> Optional[CodeAnalysis]:
        """Analizira generisani kod"""
        try:
            if code_id not in self.generated_codes:
                logger.error(f"❌ Generisani kod {code_id} nije pronađen")
                return None
            
            generated_code = self.generated_codes[code_id]
            code = generated_code.generated_code
            
            # Osnovna analiza
            lines = code.split('\n')
            line_count = len(lines)
            
            # Broj funkcija i klasa
            function_count = len(re.findall(r'def\s+\w+', code))
            class_count = len(re.findall(r'class\s+\w+', code))
            
            # Proveri sintaksu
            syntax_valid = True
            errors = []
            try:
                ast.parse(code)
            except SyntaxError as e:
                syntax_valid = False
                errors.append(f"Syntax error: {e}")
            
            # Jednostavna kompleksnost
            complexity_score = (function_count + class_count) / max(line_count, 1) * 100
            
            # Predlozi za poboljšanje
            suggestions = []
            if line_count > 200:
                suggestions.append("Kod je dugačak, razmotrite refaktorisanje")
            if function_count > 10:
                suggestions.append("Mnogo funkcija, razmotrite grupisanje")
            if class_count > 5:
                suggestions.append("Mnogo klasa, razmotrite nasleđivanje")
            
            # Kreiraj analizu
            analysis = CodeAnalysis(
                code_id=code_id,
                syntax_valid=syntax_valid,
                complexity_score=complexity_score,
                line_count=line_count,
                function_count=function_count,
                class_count=class_count,
                suggestions=suggestions,
                errors=errors
            )
            
            self.code_analyses[code_id] = analysis
            
            logger.info(f"✅ Kod analiziran: {code_id}")
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Greška pri analizi koda: {e}")
            return None
    
    def get_code_suggestions(self, user_request: str) -> List[CodeTemplate]:
        """Vraća predloge template-a na osnovu korisničkog zahteva"""
        try:
            suggestions = []
            user_request_lower = user_request.lower()
            
            for template in self.code_templates.values():
                # Proveri tagove
                tag_match = any(tag.lower() in user_request_lower for tag in template.tags)
                
                # Proveri opis
                desc_match = any(word.lower() in template.description.lower() 
                               for word in user_request_lower.split())
                
                if tag_match or desc_match:
                    suggestions.append(template)
            
            # Sortiraj po relevantnosti
            suggestions.sort(key=lambda x: len([tag for tag in x.tags 
                                             if tag.lower() in user_request_lower]), reverse=True)
            
            return suggestions[:5]  # Vraćaj top 5
            
        except Exception as e:
            logger.error(f"❌ Greška pri dohvatanju predloga: {e}")
            return []
    
    def create_custom_template(self, template: CodeTemplate) -> bool:
        """Kreira custom template"""
        try:
            if template.id in self.code_templates:
                logger.warning(f"⚠️ Template sa ID {template.id} već postoji")
                return False
            
            self.code_templates[template.id] = template
            self._save_templates()
            
            logger.info(f"✅ Custom template dodato: {template.id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Greška pri dodavanju custom template-a: {e}")
            return False
    
    def get_template_categories(self) -> List[str]:
        """Vraća listu kategorija template-a"""
        try:
            categories = set(template.category for template in self.code_templates.values())
            return sorted(list(categories))
        except Exception as e:
            logger.error(f"❌ Greška pri dohvatanju kategorija: {e}")
            return []
    
    def get_templates_by_category(self, category: str) -> List[CodeTemplate]:
        """Vraća template-e po kategoriji"""
        try:
            return [template for template in self.code_templates.values() 
                   if template.category == category]
        except Exception as e:
            logger.error(f"❌ Greška pri dohvatanju template-a po kategoriji: {e}")
            return []

# Globalna instanca
code_generation_engine = None

def get_code_generation_engine() -> CodeGenerationEngine:
    """Vraća globalnu instancu Code Generation Engine-a"""
    global code_generation_engine
    if code_generation_engine is None:
        code_generation_engine = CodeGenerationEngine()
    return code_generation_engine
