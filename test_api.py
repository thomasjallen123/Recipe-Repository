#!/usr/bin/env python
"""
Integration test script for Recipe Repository API
Run this after deploying the corrected backend to verify everything works
"""

import requests
import json
import sys
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


class APITester:
    """Test Recipe Repository API endpoints"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_user = {
            "username": f"testuser_{datetime.now().timestamp()}",
            "email": f"test_{datetime.now().timestamp()}@example.com",
            "password": "TestPassword123"
        }
        self.test_recipe_id = None
        self.passed = 0
        self.failed = 0
    
    def log(self, message, color=Colors.BLUE):
        """Print colored log message"""
        print(f"{color}{message}{Colors.END}")
    
    def test(self, name, condition, details=""):
        """Record test result"""
        if condition:
            self.log(f"✓ {name}", Colors.GREEN)
            self.passed += 1
        else:
            self.log(f"✗ {name}", Colors.RED)
            if details:
                self.log(f"  Details: {details}", Colors.YELLOW)
            self.failed += 1
    
    def run_all(self):
        """Run all tests"""
        self.log("\n" + "="*60, Colors.BLUE)
        self.log("Recipe Repository API Integration Tests", Colors.BLUE)
        self.log("="*60 + "\n", Colors.BLUE)
        
        # Health checks
        self.test_health()
        
        # Authentication
        self.test_registration()
        self.test_login()
        self.test_get_current_user()
        
        # Recipes
        self.test_get_recipes()
        self.test_search_recipes()
        self.test_get_recipe_by_id()
        
        # Collections (requires login)
        self.test_save_recipe()
        self.test_get_collections()
        self.test_is_recipe_saved()
        self.test_unsave_recipe()
        
        # Logout
        self.test_logout()
        
        # Results
        self.print_summary()
    
    def test_health(self):
        """Test health check endpoint"""
        self.log("\n--- Health Checks ---", Colors.BLUE)
        try:
            response = self.session.get(f"{self.base_url}/")
            self.test("Welcome endpoint", response.status_code == 200)
            
            response = self.session.get(f"{self.base_url}/health")
            self.test("Health check endpoint", response.status_code == 200)
            
        except Exception as e:
            self.test("Health checks", False, str(e))
    
    def test_registration(self):
        """Test user registration"""
        self.log("\n--- Authentication: Registration ---", Colors.BLUE)
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/register",
                json=self.test_user
            )
            self.test("Register new user", response.status_code == 201)
            
            # Try duplicate registration
            response = self.session.post(
                f"{self.base_url}/api/auth/register",
                json=self.test_user
            )
            self.test("Reject duplicate username", response.status_code == 409)
            
        except Exception as e:
            self.test("Registration", False, str(e))
    
    def test_login(self):
        """Test user login"""
        self.log("\n--- Authentication: Login ---", Colors.BLUE)
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json={
                    "username": self.test_user["username"],
                    "password": self.test_user["password"]
                }
            )
            self.test("Login successful", response.status_code == 200)
            
            # Test invalid password
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json={
                    "username": self.test_user["username"],
                    "password": "wrongpassword"
                }
            )
            self.test("Reject invalid password", response.status_code == 401)
            
        except Exception as e:
            self.test("Login", False, str(e))
    
    def test_get_current_user(self):
        """Test get current user endpoint"""
        self.log("\n--- Authentication: Current User ---", Colors.BLUE)
        try:
            response = self.session.get(f"{self.base_url}/api/auth/me")
            self.test("Get current user (authenticated)", response.status_code == 200)
            
            if response.status_code == 200:
                user = response.json()
                self.test("User has email", "email" in user)
                self.test("User has username", "username" in user)
            
        except Exception as e:
            self.test("Get current user", False, str(e))
    
    def test_get_recipes(self):
        """Test get recipes endpoint"""
        self.log("\n--- Recipes: List ---", Colors.BLUE)
        try:
            # Get first page
            response = self.session.get(f"{self.base_url}/api/recipes?page=1&per_page=5")
            self.test("Get recipes (paginated)", response.status_code == 200)
            
            if response.status_code == 200:
                data = response.json()
                self.test("Response has recipes list", "recipes" in data)
                self.test("Response has pagination info", "total" in data and "pages" in data)
                
                # Save first recipe ID for later tests
                if data.get("recipes"):
                    self.test_recipe_id = data["recipes"][0]["id"]
                    self.test("Recipe has required fields", all(
                        key in data["recipes"][0] 
                        for key in ["id", "title", "cuisine"]
                    ))
            
        except Exception as e:
            self.test("Get recipes", False, str(e))
    
    def test_search_recipes(self):
        """Test search recipes endpoint"""
        self.log("\n--- Recipes: Search ---", Colors.BLUE)
        try:
            response = self.session.get(f"{self.base_url}/api/recipes/search?q=chicken&page=1")
            
            if response.status_code == 200:
                self.test("Search recipes (valid query)", True)
            else:
                self.test("Search recipes", response.status_code in [200, 404])
            
            # Test invalid search (too short)
            response = self.session.get(f"{self.base_url}/api/recipes/search?q=a")
            self.test("Reject search query < 2 chars", response.status_code == 400)
            
        except Exception as e:
            self.test("Search recipes", False, str(e))
    
    def test_get_recipe_by_id(self):
        """Test get single recipe endpoint"""
        self.log("\n--- Recipes: Get by ID ---", Colors.BLUE)
        
        if not self.test_recipe_id:
            self.log("  (Skipped - no recipe ID)", Colors.YELLOW)
            return
        
        try:
            response = self.session.get(f"{self.base_url}/api/recipes/{self.test_recipe_id}")
            self.test("Get recipe by ID", response.status_code == 200)
            
            if response.status_code == 200:
                recipe = response.json()
                self.test("Recipe has ingredients", "ingredients" in recipe)
                self.test("Recipe has instructions", "instructions" in recipe)
            
            # Test invalid ID
            response = self.session.get(f"{self.base_url}/api/recipes/999999")
            self.test("Handle invalid recipe ID (404)", response.status_code == 404)
            
        except Exception as e:
            self.test("Get recipe by ID", False, str(e))
    
    def test_save_recipe(self):
        """Test save recipe endpoint"""
        self.log("\n--- Collections: Save ---", Colors.BLUE)
        
        if not self.test_recipe_id:
            self.log("  (Skipped - no recipe ID)", Colors.YELLOW)
            return
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/collections/save/{self.test_recipe_id}"
            )
            self.test("Save recipe", response.status_code == 200)
            
            # Try saving again
            response = self.session.post(
                f"{self.base_url}/api/collections/save/{self.test_recipe_id}"
            )
            self.test("Handle already-saved recipe", response.status_code == 200)
            
        except Exception as e:
            self.test("Save recipe", False, str(e))
    
    def test_get_collections(self):
        """Test get user collections endpoint"""
        self.log("\n--- Collections: Get ---", Colors.BLUE)
        try:
            response = self.session.get(f"{self.base_url}/api/collections")
            self.test("Get user collections", response.status_code == 200)
            
            if response.status_code == 200:
                data = response.json()
                self.test("Collections response is list", isinstance(data.get("recipes"), list))
            
        except Exception as e:
            self.test("Get collections", False, str(e))
    
    def test_is_recipe_saved(self):
        """Test check if recipe is saved endpoint"""
        self.log("\n--- Collections: Is Saved ---", Colors.BLUE)
        
        if not self.test_recipe_id:
            self.log("  (Skipped - no recipe ID)", Colors.YELLOW)
            return
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/collections/is-saved/{self.test_recipe_id}"
            )
            self.test("Check if recipe is saved", response.status_code == 200)
            
            if response.status_code == 200:
                data = response.json()
                self.test("Response has is_saved flag", "is_saved" in data)
            
        except Exception as e:
            self.test("Is recipe saved", False, str(e))
    
    def test_unsave_recipe(self):
        """Test unsave recipe endpoint"""
        self.log("\n--- Collections: Unsave ---", Colors.BLUE)
        
        if not self.test_recipe_id:
            self.log("  (Skipped - no recipe ID)", Colors.YELLOW)
            return
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/collections/unsave/{self.test_recipe_id}"
            )
            self.test("Unsave recipe", response.status_code == 200)
            
            # Try unsaving again
            response = self.session.post(
                f"{self.base_url}/api/collections/unsave/{self.test_recipe_id}"
            )
            self.test("Handle not-saved recipe", response.status_code == 200)
            
        except Exception as e:
            self.test("Unsave recipe", False, str(e))
    
    def test_logout(self):
        """Test logout endpoint"""
        self.log("\n--- Authentication: Logout ---", Colors.BLUE)
        try:
            response = self.session.post(f"{self.base_url}/api/auth/logout")
            self.test("Logout successful", response.status_code == 200)
            
        except Exception as e:
            self.test("Logout", False, str(e))
    
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        
        self.log("\n" + "="*60, Colors.BLUE)
        self.log("Test Results", Colors.BLUE)
        self.log("="*60, Colors.BLUE)
        
        color = Colors.GREEN if self.failed == 0 else Colors.YELLOW
        self.log(f"Passed: {self.passed}/{total} ({percentage:.1f}%)", color)
        
        if self.failed > 0:
            self.log(f"Failed: {self.failed}/{total}", Colors.RED)
        
        self.log("="*60 + "\n", Colors.BLUE)
        
        return self.failed == 0


def main():
    """Run tests"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:5000"
    
    print(f"\nTesting API at: {base_url}\n")
    
    tester = APITester(base_url)
    success = tester.run_all()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
