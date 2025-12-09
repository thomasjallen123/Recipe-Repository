// src/services/mockData.js
const cuisines = ["Italian", "Mexican", "Indian", "Chinese", "American", "Thai", "Japanese", "French"]
const ingredients = ["chicken", "beef", "pasta", "rice", "tomato", "cheese", "garlic", "onion", "egg", "shrimp", "potato", "carrot"]

export const mockRecipes = [
  {
    id: 1, title: "Classic Spaghetti Carbonara", cuisine: "Italian", prepTime: 10, cookTime: 15, servings: 4,
    image: "https://images.unsplash.com/photo-1621996346565-e3dbc44ae37b?w=800",
    ingredients: [{ name: "spaghetti", quantity: 400, unit: "g" }, { name: "eggs", quantity: 4 }, { name: "pancetta", quantity: 200, unit: "g" }],
    instructions: "Boil pasta. Fry pancetta. Mix eggs and cheese. Toss together."
  },
  {
    id: 2, title: "Penne Arrabbiata", cuisine: "Italian", prepTime: 10, cookTime: 20, servings: 4,
    image: "https://images.unsplash.com/photo-1473093226795-af9932fe5856?w=800",
    ingredients: [{ name: "penne", quantity: 500, unit: "g" }, { name: "tomatoes", quantity: 800, unit: "g" }],
    instructions: "Make spicy tomato sauce. Toss with penne."
  },
  ...Array(298).fill(null).map((_, i) => ({
    id: i + 3,
    title: `${cuisines[i % 8]} ${ingredients[i % 12]} Dish #${i + 1}`,
    cuisine: cuisines[i % 8],
    prepTime: 5 + (i % 25),
    cookTime: 15 + (i % 50),
    servings: 2 + (i % 5),
    image: `https://images.unsplash.com/photo-15${i % 10}4674900247-0877df9cc836?w=800`,
    ingredients: [
      { name: ingredients[i % 12], quantity: 100 + (i % 400), unit: "g" },
      { name: ingredients[(i + 1) % 12], quantity: 50 + (i % 200), unit: "g" }
    ],
    instructions: `Cook ${ingredients[i % 12]} with love. Serve hot.`,
    isSaved: Math.random() < 0.05
  }))
]