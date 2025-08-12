// Mock roast data for the MVP
export const mockRoasts = [
  "Hey {name}, I'd roast you, but my mom said I shouldn't burn trash! 🔥",
  "{name}? More like {name}-sty! Even autocorrect doesn't want to acknowledge you! 😂",
  "I was going to make fun of {name}, but then I realized nature already did! 🌿",
  "{name}, you're like a software update - nobody wants you, but you keep showing up anyway! 💻",
  "Dear {name}, I'd call you average, but that would be an insult to average people! 📊",
  "{name}, you're the reason they put directions on shampoo bottles! 🧴",
  "If {name} were a spice, you'd be flour - bland and unnecessary! 🌶️",
  "{name}, you're like a participation trophy - everyone gets one, but nobody really wants it! 🏆",
  "Hey {name}, I heard you went to the library to find your name in the phone book! 📚",
  "{name}, you're so unique, just like everyone else! ✨"
];

// Function to get a random roast with name replacement
export const generateRandomRoast = (name) => {
  if (!name || name.trim() === '') {
    return "Enter a name first, genius! Even I need something to work with! 😏";
  }
  
  const randomIndex = Math.floor(Math.random() * mockRoasts.length);
  const selectedRoast = mockRoasts[randomIndex];
  
  // Replace {name} placeholder with actual name
  return selectedRoast.replace(/{name}/g, name.trim());
};

// Simulated delay for "AI thinking" effect
export const simulateAIDelay = (callback, delay = 2000) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const result = callback();
      resolve(result);
    }, delay);
  });
};