from together import Together
from langchain.prompts import PromptTemplate
import json
import os
import tiktoken
from typing import Dict, List, Tuple
import re
from ..core.config import settings
from ..core.database import db_manager
from ..core.domains import DOMAIN_DESCRIPTIONS, DOMAIN_TO_TABLES_MAPPING
from ..core.prompts import PROMPT_TEMPLATE, SIMPLE_PROMPT_TEMPLATE

class SQLAssistantService:
    def __init__(self):
        self.llm_client = Together(api_key=settings.TOGETHER_API_KEY)
        self.db = db_manager.get_database()
        
        # Initialiser le tokenizer
        try:
            self.enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
        except:
            self.enc = tiktoken.get_encoding("cl100k_base")
            
        self.cache_data = self._load_cache()
        
    def _load_cache(self) -> Dict:
        try:
            if os.path.exists(settings.CACHE_FILE):
                with open(settings.CACHE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception:
            return {}
            
    def _save_cache(self):
        try:
            with open(settings.CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Cache save error: {e}")
            
    def _ask_llm(self, prompt: str) -> str:
        try:
            response = self.llm_client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2048
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"LLM Error: {str(e)}")
            
    def _count_tokens(self, text: str) -> int:
        return len(self.enc.encode(text))
        
    def ask_question(self, question: str) -> Tuple[str, str, float, int, bool]:
        # Vérifier le cache en premier
        if question in self.cache_data:
            cached = self.cache_data[question]
            return cached["sql"], cached["response"], 0.0, 0, True

        # Essayer de faire correspondre un modèle
        sql_from_template, variables = self.match_template_question(question)
        if sql_from_template:
            print(f"💡 Requête générée depuis template : {sql_from_template}")
            response = self.db.run(sql_from_template)
            return sql_from_template, response, 0.0, 0, False

        try:
            # Identifier les domaines et construire le prompt
            prompt = self._build_prompt(question)
            
            # Obtenir la requête SQL depuis le LLM
            sql_query = self._ask_llm(prompt)
            
            # Exécuter la requête SQL
            response = self.db.run(sql_query)
            
            # Calculer le coût et les jetons
            prompt_tokens = self._count_tokens(prompt)
            response_tokens = self._count_tokens(response)
            total_tokens = prompt_tokens + response_tokens
            cost = self._calculate_cost(total_tokens)
            
            # Mettre en cache la nouvelle question
            self.cache_data[question] = {"sql": sql_query, "response": response}
            self._save_cache()
            
            return sql_query, response, cost, total_tokens, False

        except Exception as e:
            return "", f"Erreur système: {str(e)}", 0.0, 0, False
                
    def _get_relevant_domains(self, query: str) -> List[str]:
        """Identifie les domaines pertinents basés sur la requête utilisateur"""
        domain_desc_str = "\n".join([f"- {name}: {desc}" for name, desc in DOMAIN_DESCRIPTIONS.items()])
        domain_prompt_content = f"""
        Based on the following user question, identify ALL relevant domains from the list below.
        Return only the names of the relevant domains, separated by commas. If no domain is relevant, return 'None'.

        User Question: {query}

        Available Domains and Descriptions:
        {domain_desc_str}

        Relevant Domains (comma-separated):
        """
        
        try:
            response = self._ask_llm(domain_prompt_content)
            domain_names = response.strip()
            
            if domain_names.lower() == 'none' or not domain_names:
                return []
            return [d.strip() for d in domain_names.split(',')]
        except Exception as e:
            print(f"Erreur lors de l'identification des domaines: {e}")
            return []

    def _build_prompt(self, question: str) -> str:
        """Construit le prompt pour le LLM."""
        relevant_domains = self._get_relevant_domains(question)
        
        if relevant_domains:
            relevant_domain_descriptions = "\n".join([
                f"- {domain}: {DOMAIN_DESCRIPTIONS[domain]}"
                for domain in relevant_domains if domain in DOMAIN_DESCRIPTIONS
            ])
            
            return PROMPT_TEMPLATE.format(
                input=question,
                table_info=self.db.get_table_info(),
                relevant_domain_descriptions=relevant_domain_descriptions,
                relations=self._load_relations()
            )
        else:
            return SIMPLE_PROMPT_TEMPLATE.format(
                input=question,
                table_info=self.db.get_table_info()
            )

    def _calculate_cost(self, tokens: int, cost_per_1000_tokens: float = 0.001) -> float:
        """Calcule le coût basé sur le nombre de jetons."""
        return (tokens / 1000) * cost_per_1000_tokens

    def _load_relations(self) -> str:
        """Charge les relations depuis un fichier ou retourne une chaîne vide"""
        try:
            with open(settings.RELATIONS_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            return ""
    
    def match_template_question(self, question: str) -> Tuple[str, dict] | Tuple[None, None]:
        """Fait correspondre une question à un modèle et extrait les variables."""
        for entry in self.cache_data:
            if 'question_pattern' in entry and 'sql_template' in entry:
                variables = self.extract_variables(question, entry['question_pattern'])
                if variables:
                    sql_query = entry['sql_template'].format(**variables)
                    return sql_query, variables
        return None, None

    @staticmethod
    def extract_variables(question: str, question_pattern: str):
        regex = question_pattern
        for var in re.findall(r"{(.*?)}", question_pattern):
            regex = regex.replace(f"{{{var}}}", r"(?P<%s>.+)" % var)
        match = re.match(regex, question, re.IGNORECASE)
        return match.groupdict() if match else None