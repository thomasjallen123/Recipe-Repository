// src/services/mockData.js
// FULL MOCK DATA — 300+ REAL-LOOKING RECIPES
// SEARCH: chicken, pasta, beef, rice, tomato, cheese, garlic, onion, spicy, quick

export const mockRecipes = [
  // REAL PASTA RECIPES
  {
    id: 1,
    title: "Classic Spaghetti Carbonara",
    cuisine: "Italian",
    prepTime: 10,
    cookTime: 15,
    servings: 4,
    image: "https://images.unsplash.com/photo-1621996346565-e3dbc44ae37b?w=800",
    ingredients: [
      { name: "spaghetti", quantity: 400, unit: "g" },
      { name: "eggs", quantity: 4, unit: "" },
      { name: "pancetta", quantity: 200, unit: "g" },
      { name: "parmesan cheese", quantity: 100, unit: "g" },
      { name: "black pepper", quantity: 1, unit: "tsp" }
    ],
    instructions: "1. Boil pasta in salted water.\n2. Fry pancetta until crispy.\n3. Mix eggs + cheese.\n4. Toss hot pasta with pancetta and egg mixture.\n5. Serve immediately.",
    isSaved: true
  },
  {
    id: 2,
    title: "Penne Arrabbiata (Spicy Tomato Pasta)",
    cuisine: "Italian",
    prepTime: 10,
    cookTime: 20,
    servings: 4,
    image: "https://images.unsplash.com/photo-1473093226795-af9932fe5856?w=800",
    ingredients: [
      { name: "penne pasta", quantity: 500, unit: "g" },
      { name: "canned tomatoes", quantity: 800, unit: "g" },
      { name: "garlic", quantity: 4, unit: "cloves" },
      { name: "red chili flakes", quantity: 2, unit: "tsp" },
      { name: "olive oil", quantity: 4, unit: "tbsp" }
    ],
    instructions: "Make angry (spicy) tomato sauce with garlic and chili. Toss with penne. Top with parsley.",
    isSaved: false
  },
  {
    id: 3,
    title: "Creamy Fettuccine Alfredo",
    cuisine: "Italian",
    prepTime: 5,
    cookTime: 15,
    servings: 4,
    image: "https://images.unsplash.com/photo-1621996346565-e3dbc44ae37b?w=800",
    ingredients: [
      { name: "fettuccine pasta", quantity: 400, unit: "g" },
      { name: "butter", quantity: 100, unit: "g" },
      { name: "heavy cream", quantity: 300, unit: "ml" },
      { name: "parmesan cheese", quantity: 150, unit: "g" },
      { name: "garlic", quantity: 2, unit: "cloves" }
    ],
    instructions: "Cook pasta. Melt butter, add cream and garlic. Stir in cheese until thick. Toss with pasta.",
    isSaved: true
  },

  // CHICKEN
  {
    id: 4,
    title: "Butter Chicken (Murgh Makhani)",
    cuisine: "Indian",
    prepTime: 20,
    cookTime: 30,
    servings: 6,
    image: "https://images.unsplash.com/photo-1603894585357-4f72cda17e21?w=800",
    ingredients: [
      { name: "chicken thighs", quantity: 1.5, unit: "kg" },
      { name: "yogurt", quantity: 200, unit: "ml" },
      { name: "butter", quantity: 100, unit: "g" },
      { name: "tomato puree", quantity: 400, unit: "ml" },
      { name: "garam masala", quantity: 2, unit: "tbsp" }
    ],
    instructions: "Marinate chicken in yogurt. Grill. Make creamy tomato sauce. Combine.",
    isSaved: true
  },
  {
    id: 5,
    title: "Chicken Tikka Masala",
    cuisine: "Indian",
    prepTime: 30,
    cookTime: 30,
    servings: 5,
    image: "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=800",
    ingredients: [
      { name: "chicken breast", quantity: 1, unit: "kg" },
      { name: "yogurt", quantity: 250, unit: "ml" },
      { name: "tomato sauce", quantity: 500, unit: "ml" },
      { name: "cream", quantity: 200, unit: "ml" }
    ],
    instructions: "Marinate and grill chicken. Simmer in spiced tomato cream sauce.",
    isSaved: false
  },

  // BEEF
  {
    id: 6,
    title: "Beef Tacos",
    cuisine: "Mexican",
    prepTime: 15,
    cookTime: 20,
    servings: 4,
    image: "https://images.unsplash.com/photo-1565299507177-b0ac667bd8d5?w=800",
    ingredients: [
      { name: "ground beef", quantity: 500, unit: "g" },
      { name: "taco shells", quantity: 12, unit: "" },
      { name: "lettuce", quantity: 1, unit: "head" },
      { name: "cheese", quantity: 200, unit: "g" },
      { name: "tomato", quantity: 2, unit: "" }
    ],
    instructions: "Brown beef with spices. Fill shells with toppings.",
    isSaved: true
  },

  // RICE
  {
    id: 7,
    title: "Chicken Fried Rice",
    cuisine: "Chinese",
    prepTime: 10,
    cookTime: 15,
    servings: 4,
    image: "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800",
    ingredients: [
      { name: "rice", quantity: 300, unit: "g" },
      { name: "chicken", quantity: 300, unit: "g" },
      { name: "eggs", quantity: 3, unit: "" },
      { name: "soy sauce", quantity: 3, unit: "tbsp" },
      { name: "peas", quantity: 100, unit: "g" }
    ],
    instructions: "Fry rice with chicken, egg, and veggies. Season with soy sauce.",
    isSaved: false
  },

  // MORE REAL ONES
  {
    id: 8,
    title: "Pad Thai",
    cuisine: "Thai",
    prepTime: 20,
    cookTime: 15,
    servings: 4,
    image: "https://images.unsplash.com/photo-1559314809-0d155395afa8?w=800",
    ingredients: [
      { name: "rice noodles", quantity: 300, unit: "g" },
      { name: "shrimp", quantity: 200, unit: "g" },
      { name: "peanuts", quantity: 50, unit: "g" },
      { name: "bean sprouts", quantity: 100, unit: "g" },
      { name: "tamarind paste", quantity: 3, unit: "tbsp" }
    ],
    instructions: "Soak noodles. Stir-fry with shrimp and sauce. Top with peanuts.",
    isSaved: true
  },

  // GENERIC BUT SEARCHABLE
  ...Array(292).fill(null).map((_, i) => {
    const titles = [
      "Garlic Butter Shrimp Pasta", "Spicy Beef Stir Fry", "Tomato Basil Soup",
      "Cheese Pizza", "Chicken Parmesan", "Beef Stroganoff", "Rice Pilaf",
      "Onion Rings", "Quick Pancakes", "Spicy Thai Noodles"
    ]
    const cuisines = ["Italian", "Mexican", "Indian", "Chinese", "American", "Thai", "Japanese"]
    const ingredients = ["chicken", "beef", "pasta", "rice", "tomato", "cheese", "garlic", "onion", "egg", "shrimp"]

    return {
      id: i + 9,
      title: titles[i % titles.length] + ` #${i + 1}`,
      cuisine: cuisines[i % cuisines.length],
      prepTime: 5 + (i % 20),
      cookTime: 15 + (i % 45),
      servings: 2 + (i % 4),
      image: `https://images.unsplash.com/photo-1547574405-1d9e2e3b6d8a?w=800&ixlib=rb-4.0.3&auto=format&fit=crop&q=80`,
      ingredients: [
        { name: ingredients[i % 10], quantity: 100 + (i % 400), unit: "g" },
        { name: ingredients[(i + 1) % 10], quantity: 50 + (i % 200), unit: "g" },
        { name: "salt", quantity: 1, unit: "tsp" }
      ],
      instructions: `Cook ${ingredients[i % 10]} with love. Season well. Serve hot.`,
      isSaved: Math.random() > 0.7
    }
  })
]