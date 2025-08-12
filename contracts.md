# AI Roast Generator - API Contracts & Integration Plan

## API Endpoints

### 1. Generate Roast
- **Endpoint**: `POST /api/generate-roast`
- **Request Body**:
  ```json
  {
    "name": "string",
    "category": "light" | "medium" | "extra_spicy"
  }
  ```
- **Response**:
  ```json
  {
    "roast": "string",
    "name": "string", 
    "category": "string",
    "timestamp": "datetime"
  }
  ```

### 2. Random Names
- **Endpoint**: `GET /api/random-names`
- **Response**:
  ```json
  {
    "names": ["string array of funny names"]
  }
  ```

## Mock Data Replacement

The following mock data in `mockData.js` will be replaced:
- `mockRoasts` array → Real AI-generated roasts from OpenRouter GPT-4o-mini
- `generateRandomRoast()` function → API call to `/api/generate-roast`
- `simulateAIDelay()` → Real API response time

## Frontend Integration Changes

1. **Replace Mock Functions**: Update roast generation to use real API
2. **Add Roast Categories**: UI for selecting Light/Medium/Extra Spicy
3. **Add Roast History**: Store last 5 roasts in localStorage
4. **Add Social Sharing**: WhatsApp & Twitter/X direct links
5. **Add Random Names**: "Surprise Me!" button with funny name suggestions
6. **Add Roast Counter**: Track daily roasts in localStorage

## New Features Implementation

### Roast History
- Store in localStorage as `roastHistory` array (max 5 items)
- Display below main roast card
- Each history item shows name, roast, category, and timestamp

### Social Share Buttons  
- WhatsApp: `https://wa.me/?text=${encodeURIComponent(shareText)}`
- Twitter/X: `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}`

### Random Name Generator
- Fetch from `/api/random-names`
- Button fills input with random funny name
- Names like "Banana Bob", "Pizza Pete", etc.

### Roast Categories
- Radio buttons or select dropdown
- Light: Family-friendly, gentle teasing
- Medium: Moderately sharp, witty
- Extra Spicy: Brutal but creative burns

### Daily Counter
- Store in localStorage as `dailyRoastCount_${today}` 
- Reset count each day
- Display as badge: "🔥 X Roasts Generated Today"

## Error Handling
- API failures fall back to mock roasts
- Network errors show user-friendly messages
- Invalid inputs blocked with validation