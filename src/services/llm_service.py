from groq import Groq
import httpx
import logging
import re

logger = logging.getLogger(__name__)

class LLMService:
    """Service để tương tác với Groq API (Free LLM)"""
    
    def __init__(self, api_key: str, model: str = "llama3-8b-8192"):
        self.client = Groq(api_key=api_key)
        self.model = model
        logger.info(f"LLMService initialized with model: {model}")

    # def __init__(self, api_key: str, model: str = "llama3-8b-8192"):
    #     http_client = httpx.Client(
    #         proxy="socks5://127.0.0.1:1080"  # đổi thành port VPN/proxy của bạn
    #     )
    #     self.client = Groq(api_key=api_key, http_client=http_client)
    #     self.model = model
    #     logger.info(f"LLMService initialized with model: {model}")

    def _remove_duplicates(self, text: str) -> str:
        """Remove duplicate paragraphs/sentences"""
        lines = text.split('\n')
        seen = set()
        unique_lines = []
        
        for line in lines:
            # Normalize line for comparison
            normalized = line.strip().lower()
            
            if normalized and normalized not in seen:
                seen.add(normalized)
                unique_lines.append(line)
            elif not normalized:  # Keep empty lines
                unique_lines.append(line)
        
        return '\n'.join(unique_lines)

    async def generate_response(self, messages: list, system_prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> dict:
        """Generate response from Groq API"""
        try:
            # Format messages
            formatted_messages = [
                {"role": "system", "content": system_prompt},
                *messages
            ]
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            content = response.choices[0].message.content
            
            logger.info(f"Generated response ({len(content)} chars)")
            return {
                "success": True,
                "content": content
            }
        
        except Exception as e:
            logger.error(f"LLM Error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def check_grammar(self, user_text: str, language: str) -> dict:
        """Check grammar using LLM"""
        
        grammar_prompt = f"""You are an expert language tutor in {language}.
Analyze this text and find grammar, spelling, and punctuation errors.

Format your response using HTML tags exactly like this:
<b>Original:</b> [user's text]
<b>Corrected:</b> [corrected version]
<b>Explanations:</b>
- [error 1 with explanation]
- [error 2 with explanation]

If NO errors, respond: "✅ Perfect! No errors found."

Do NOT use markdown (no **, no __). Use only the HTML tags shown above.
Do NOT repeat explanations. Do NOT add anything else.

Text: {user_text}"""
        
        result = await self.generate_response(
            messages=[{"role": "user", "content": user_text}],
            system_prompt=grammar_prompt,
            temperature=0.2,
            max_tokens=300
        )

        return result
