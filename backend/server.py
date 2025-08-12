from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import aiohttp
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# OpenRouter configuration
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class RoastRequest(BaseModel):
    name: str
    category: str = "medium"  # light, medium, extra_spicy

class RoastResponse(BaseModel):
    roast: str
    name: str
    category: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Roast generation prompts based on category
ROAST_PROMPTS = {
    "light": """You are a witty but gentle roast generator. Generate a playful, light-hearted roast for the name '{name}'. 
    Keep it fun, family-friendly, and harmless. Use wordplay and clever observations. Add appropriate emojis. 
    Keep it under 50 words and make it genuinely funny without being mean.""",
    
    "medium": """You are a sassy roast generator. Generate a moderately sharp but still playful roast for the name '{name}'. 
    Be witty, use clever observations, and add some bite while keeping it entertaining. Add appropriate emojis. 
    Keep it under 50 words and make it burn just right - not too soft, not too harsh.""",
    
    "extra_spicy": """You are a savage roast generator. Generate a hilariously brutal but creative roast for the name '{name}'. 
    Be ruthlessly witty, use sharp humor, and don't hold back - but keep it clever and creative, not just mean. 
    Add fire emojis. Keep it under 50 words and make it absolutely devastating in the funniest way possible."""
}

async def generate_ai_roast(name: str, category: str = "medium") -> str:
    """Generate a roast using OpenRouter GPT-4o-mini"""
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenRouter API key not configured")
    
    prompt = ROAST_PROMPTS.get(category, ROAST_PROMPTS["medium"]).format(name=name)
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "AI Roast Generator"
    }
    
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system", 
                "content": "You are a witty roast generator. Keep responses short, funny, and creative. Always include emojis."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 100,
        "temperature": 0.9,
        "top_p": 1,
        "frequency_penalty": 0.5,
        "presence_penalty": 0.5
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(OPENROUTER_BASE_URL, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    roast = data['choices'][0]['message']['content'].strip()
                    return roast
                else:
                    error_text = await response.text()
                    logger.error(f"OpenRouter API error {response.status}: {error_text}")
                    raise HTTPException(status_code=500, detail=f"AI service error: {response.status}")
    
    except Exception as e:
        logger.error(f"Error calling OpenRouter API: {str(e)}")
        # Fallback to mock roasts if API fails
        fallback_roasts = {
            "light": f"Hey {name}, you're like a human participation trophy - everyone gets one! 🏆",
            "medium": f"{name}, you're so unique, just like everyone else! ✨",
            "extra_spicy": f"{name}, I'd roast you harder, but my mom said not to burn trash! 🔥"
        }
        return fallback_roasts.get(category, fallback_roasts["medium"])

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

@api_router.post("/generate-roast", response_model=RoastResponse)
async def generate_roast(request: RoastRequest):
    """Generate a roast using AI"""
    try:
        if not request.name.strip():
            raise HTTPException(status_code=400, detail="Name is required")
        
        # Generate roast using OpenRouter
        roast = await generate_ai_roast(request.name, request.category)
        
        response = RoastResponse(
            roast=roast,
            name=request.name,
            category=request.category
        )
        
        # Optionally store in database for analytics
        try:
            await db.roasts.insert_one(response.dict())
        except Exception as e:
            logger.warning(f"Failed to store roast in database: {e}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating roast: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate roast")

@api_router.get("/random-names")
async def get_random_names():
    """Get a list of random funny names for the 'Surprise Me' feature"""
    funny_names = [
        "Banana Bob", "Pizza Pete", "Disco Danny", "Muffin Mike", "Taco Tom",
        "Waffle Wayne", "Pickle Paul", "Donut Dave", "Cookie Carl", "Pretzel Pat",
        "Noodle Nick", "Bagel Bill", "Cupcake Chris", "Pancake Phil", "Burrito Ben",
        "Sushi Sam", "Cheese Charlie", "Bacon Barry", "Sandwich Steve", "Yogurt Yuki"
    ]
    return {"names": funny_names}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()