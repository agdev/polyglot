import json
from pathlib import Path
from typing import Dict, List, Optional

class DictionaryManager:
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path or "data/dictionary.json")
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.dictionary: Dict[str, Dict[str, List[str]]] = self._load_dictionary()
    
    def _load_dictionary(self) -> Dict[str, Dict[str, List[str]]]:
        """Load dictionary from file or create new if doesn't exist"""
        if self.storage_path.exists():
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_dictionary(self):
        """Save dictionary to file"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.dictionary, f, ensure_ascii=False, indent=2)
    
    def add_entry(self, source_lang: str, target_lang: str, word: str, translation: str):
        """Add a word and its translation to the dictionary"""
        if source_lang not in self.dictionary:
            self.dictionary[source_lang] = {}
        
        if target_lang not in self.dictionary[source_lang]:
            self.dictionary[source_lang][target_lang] = []
        
        entry = f"{word} → {translation}"
        if entry not in self.dictionary[source_lang][target_lang]:
            self.dictionary[source_lang][target_lang].append(entry)
            self._save_dictionary()
    
    def get_entries(self, source_lang: str, target_lang: str) -> List[str]:
        """Get all entries for a language pair"""
        return self.dictionary.get(source_lang, {}).get(target_lang, [])
    
    def export_dictionary(self) -> str:
        """Export dictionary as formatted string"""
        output = []
        for source_lang, translations in self.dictionary.items():
            output.append(f"# {source_lang.upper()} Dictionary")
            for target_lang, entries in translations.items():
                output.append(f"\n## Translations to {target_lang.upper()}")
                for entry in entries:
                    output.append(f"- {entry}")
            output.append("\n")
        return "\n".join(output)
