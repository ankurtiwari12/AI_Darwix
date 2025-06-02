from transformers import pipeline
import os
from typing import List

class TitleSuggestionService:
    def __init__(self):
        self.generator = pipeline(
            "text2text-generation",
            model="facebook/bart-large-cnn",
            token=os.getenv("HUGGINGFACE_TOKEN")
        )

    def generate_title_suggestions(self, content: str, num_suggestions: int = 3) -> List[str]:
        # Prepare the input text
        input_text = f"summarize: {content}"
        
        # Generate multiple suggestions
        suggestions = []
        for _ in range(num_suggestions):
            result = self.generator(
                input_text,
                max_length=50,
                num_return_sequences=1,
                temperature=0.7
            )
            title = result[0]['generated_text'].strip()
            suggestions.append(title)
        
        return suggestions 