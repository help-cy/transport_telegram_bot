import json
import logging
from typing import Dict, Optional

from openai import AsyncOpenAI

from src.models.categories import CATEGORIES, get_all_categories, get_subcategories_for_category
from src.config.settings import settings


logger = logging.getLogger(__name__)


class AIVisionService:
    
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.openai.api_key
        )
        self.model = settings.openai.model
        self.max_tokens = settings.openai.max_tokens
        self.temperature = settings.openai.temperature
    
    def _build_system_prompt(self) -> str:
        categories_info = []
        for category, subcategories in CATEGORIES.items():
            subcats_str = ", ".join(subcategories)
            categories_info.append(
                f"- {category}: [{subcats_str}]"
            )
        
        categories_list = "\n".join(categories_info)
        
        system_prompt = f"""You are an AI assistant that analyzes photos of municipal infrastructure problems.

Your task is to:
1. Analyze the photo and identify the main problem
2. Select the most appropriate category from the available options
3. Select the most appropriate subcategory within that category
4. Generate a clear, concise description of the problem in English

Available categories and their subcategories:
{categories_list}

You must respond with a JSON object containing:
- "category": one of the main categories listed above
- "subcategory": one of the subcategories for the selected category
- "description": a clear description of the problem (2-3 sentences)

If you're unsure, use "Other" as the category or subcategory.
Focus on infrastructure, roads, utilities, and public facilities issues."""
        
        return system_prompt
    
    def _validate_response(
        self,
        category: str,
        subcategory: str
    ) -> tuple[str, str]:
        if category not in CATEGORIES:
            logger.warning(
                msg=f"Invalid category '{category}', defaulting to 'Other'"
            )
            category = "Other"
        
        valid_subcategories = CATEGORIES[category]
        if subcategory not in valid_subcategories:
            logger.warning(
                msg=f"Invalid subcategory '{subcategory}' for category '{category}', defaulting to 'Other'"
            )
            subcategory = "Other" if "Other" in valid_subcategories else valid_subcategories[0]
        
        return category, subcategory
    
    async def analyze_problem_photo(
        self,
        photo_url: str
    ) -> Dict[str, str]:
        try:
            system_prompt = self._build_system_prompt()
            
            logger.info(
                msg=f"Analyzing photo with OpenAI Vision: {photo_url}"
            )
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this photo and identify the municipal problem. Respond with JSON containing category, subcategory, and description."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": photo_url,
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                response_format={
                    "type": "json_object"
                }
            )
            
            content = response.choices[0].message.content
            
            if not content:
                raise ValueError("Empty response from OpenAI")
            
            logger.debug(
                msg=f"OpenAI response: {content}"
            )
            
            result = json.loads(content)
            
            category = result.get(
                "category",
                "Other"
            )
            subcategory = result.get(
                "subcategory",
                "Other"
            )
            description = result.get(
                "description",
                "Infrastructure issue detected"
            )
            
            category, subcategory = self._validate_response(
                category=category,
                subcategory=subcategory
            )
            
            logger.info(
                msg=f"AI analysis result: {category} -> {subcategory}"
            )
            
            return {
                "category": category,
                "subcategory": subcategory,
                "description": description
            }
            
        except Exception as e:
            logger.error(
                msg=f"Error analyzing photo with OpenAI: {e}",
                exc_info=True
            )
            
            fallback_category = "Other"
            fallback_subcategories = get_subcategories_for_category(
                category=fallback_category
            )
            
            return {
                "category": fallback_category,
                "subcategory": fallback_subcategories[0],
                "description": "Infrastructure issue detected. AI analysis failed, please review manually."
            }
