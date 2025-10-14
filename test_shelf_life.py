"""
USDA FoodKeeper Database Shelf-Life Test
Tests hypothesis: We believe that the expiration dates for fresh food produce can be estimated using an open-source shelf-life database
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class TestItem:
    """Represents a food item to test"""
    name: str
    category: str
    search_variants: List[str]
    
    
@dataclass
class MatchResult:
    """Results of a mapping attempt"""
    test_item: str
    matched: bool
    foodkeeper_id: Optional[str] = None
    foodkeeper_name: Optional[str] = None
    match_type: Optional[str] = None  # exact, keyword, fuzzy
    shelf_life_data: Optional[Dict] = None
    

class FoodKeeperDB:
    """Handles USDA FoodKeeper json with caching"""
    
    def __init__(self, json_path: str):
        self.json_path = Path(json_path)
        self.data = self._load_data()
        self.cache = {}
        self._build_search_index()
        
    def _load_data(self) -> Dict:
        """Load the FoodKeeper JSON data"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _build_search_index(self):
        """Build search indices for efficient lookup"""
        self.name_index = {}
        self.keyword_index = {}
        
        for product in self.data.get('product_data', []):
            prod_id = product['id']
            name = product['name'].lower()
            
            # Index by name
            if name not in self.name_index:
                self.name_index[name] = []
            self.name_index[name].append(product)
            
            # Index by keywords
            if product.get('keywords'):
                keywords = product['keywords'].lower().split(',')
                for keyword in keywords:
                    keyword = keyword.strip()
                    if keyword not in self.keyword_index:
                        self.keyword_index[keyword] = []
                    self.keyword_index[keyword].append(product)
    
    def _extract_shelf_life(self, product: Dict) -> Dict:
        """Extract relevant shelf life information"""
        return {
            'refrigerate': product.get('from_date_of_purchase_refrigerate_output_display_only') 
                          or product.get('refrigerate_output_display_only'),
            'freeze': product.get('from_date_of_purchase_freeze_output_display_only') 
                     or product.get('freeze_output_display_only'),
            'pantry': product.get('from_date_of_purchase_pantry_output_display_only') 
                     or product.get('pantry_output_display_only'),
            'category': product.get('category_name_display_only'),
            'subcategory': product.get('subcategory_name_display_only')
        }
    
    def search(self, item_name: str) -> Optional[MatchResult]:
        """Search for a food item with caching"""
        # Check cache first
        cache_key = item_name.lower()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = self._perform_search(item_name)
        self.cache[cache_key] = result
        return result
    
    def _perform_search(self, item_name: str) -> Optional[MatchResult]:
        """Perform the actual search with multiple strategies"""
        item_lower = item_name.lower()
        
        # Strategy 1: Exact name match
        if item_lower in self.name_index:
            product = self.name_index[item_lower][0]
            return MatchResult(
                test_item=item_name,
                matched=True,
                foodkeeper_id=product['id'],
                foodkeeper_name=product['name'],
                match_type='exact',
                shelf_life_data=self._extract_shelf_life(product)
            )
        
        # Strategy 2: Keyword match
        for keyword, products in self.keyword_index.items():
            if keyword in item_lower or item_lower in keyword:
                product = products[0]
                return MatchResult(
                    test_item=item_name,
                    matched=True,
                    foodkeeper_id=product['id'],
                    foodkeeper_name=product['name'],
                    match_type='keyword',
                    shelf_life_data=self._extract_shelf_life(product)
                )
        
        # Strategy 3: Fuzzy match (partial name matching)
        for name, products in self.name_index.items():
            if item_lower in name or name in item_lower:
                product = products[0]
                return MatchResult(
                    test_item=item_name,
                    matched=True,
                    foodkeeper_id=product['id'],
                    foodkeeper_name=product['name'],
                    match_type='fuzzy',
                    shelf_life_data=self._extract_shelf_life(product)
                )
        
        # No match found
        return MatchResult(test_item=item_name, matched=False)


class TestRunner:
    """Orchestrates the testing process"""
    
    def __init__(self, db: FoodKeeperDB):
        self.db = db
        self.test_items = self._create_test_suite()
        
    def _create_test_suite(self) -> List[TestItem]:
        """Curate 50 diverse test items across categories"""
        return [
            # Dairy
            TestItem("milk", "dairy", ["milk", "whole milk"]),
            TestItem("cheddar cheese", "dairy", ["cheese", "cheddar"]),
            TestItem("yogurt", "dairy", ["yogurt"]),
            TestItem("butter", "dairy", ["butter"]),
            TestItem("eggs", "dairy", ["eggs", "egg"]),
            
            # Meat
            TestItem("chicken breast", "meat", ["chicken", "breast"]),
            TestItem("ground beef", "meat", ["beef", "ground"]),
            TestItem("bacon", "meat", ["bacon"]),
            TestItem("pork chops", "meat", ["pork"]),
            TestItem("steak", "meat", ["steak", "beef"]),
            
            # Seafood
            TestItem("salmon", "seafood", ["salmon"]),
            TestItem("shrimp", "seafood", ["shrimp"]),
            TestItem("tuna", "seafood", ["tuna"]),
            TestItem("cod", "seafood", ["cod"]),
            TestItem("lobster", "seafood", ["lobster"]),
            
            # Produce - Vegetables
            TestItem("lettuce", "produce", ["lettuce"]),
            TestItem("tomatoes", "produce", ["tomato", "tomatoes"]),
            TestItem("carrots", "produce", ["carrot", "carrots"]),
            TestItem("broccoli", "produce", ["broccoli"]),
            TestItem("spinach", "produce", ["spinach"]),
            TestItem("onions", "produce", ["onion", "onions"]),
            TestItem("potatoes", "produce", ["potato", "potatoes"]),
            TestItem("bell peppers", "produce", ["pepper", "peppers"]),
            
            # Produce - Fruits
            TestItem("apples", "produce", ["apple", "apples"]),
            TestItem("bananas", "produce", ["banana", "bananas"]),
            TestItem("oranges", "produce", ["orange", "oranges"]),
            TestItem("strawberries", "produce", ["strawberry", "strawberries"]),
            TestItem("grapes", "produce", ["grape", "grapes"]),
            TestItem("blueberries", "produce", ["blueberry", "blueberries"]),
            
            # Baked Goods
            TestItem("bread", "baked", ["bread"]),
            TestItem("bagels", "baked", ["bagel", "bagels"]),
            TestItem("muffins", "baked", ["muffin", "muffins"]),
            
            # Frozen Foods
            TestItem("ice cream", "frozen", ["ice cream"]),
            TestItem("frozen pizza", "frozen", ["pizza"]),
            TestItem("frozen vegetables", "frozen", ["vegetables", "frozen"]),
            
            # Condiments
            TestItem("ketchup", "condiments", ["ketchup"]),
            TestItem("mayonnaise", "condiments", ["mayonnaise", "mayo"]),
            TestItem("mustard", "condiments", ["mustard"]),
            TestItem("soy sauce", "condiments", ["soy sauce"]),
            
            # Beverages
            TestItem("orange juice", "beverages", ["juice", "orange"]),
            TestItem("apple juice", "beverages", ["juice", "apple"]),
            TestItem("milk alternative", "beverages", ["almond milk", "soy milk"]),
            
            # Deli
            TestItem("deli ham", "deli", ["ham", "deli"]),
            TestItem("turkey slices", "deli", ["turkey"]),
            TestItem("salami", "deli", ["salami"]),
            
            # Pantry Staples
            TestItem("rice", "pantry", ["rice"]),
            TestItem("pasta", "pantry", ["pasta"]),
            TestItem("flour", "pantry", ["flour"]),
            TestItem("sugar", "pantry", ["sugar"]),
            TestItem("cooking oil", "pantry", ["oil"]),
        ]
    
    def run_tests(self) -> Tuple[List[MatchResult], Dict]:
        """Execute all tests and return results with statistics"""
        results = []
        
        for test_item in self.test_items:
            # Try primary name first
            result = self.db.search(test_item.name)
            
            # If no match, try variants
            if not result.matched:
                for variant in test_item.search_variants:
                    result = self.db.search(variant)
                    if result.matched:
                        break
            
            results.append(result)
        
        stats = self._calculate_statistics(results)
        return results, stats
    
    def _calculate_statistics(self, results: List[MatchResult]) -> Dict:
        """Calculate test statistics"""
        total = len(results)
        matched = sum(1 for r in results if r.matched)
        
        match_types = {}
        for r in results:
            if r.matched and r.match_type:
                match_types[r.match_type] = match_types.get(r.match_type, 0) + 1
        
        return {
            'total_items': total,
            'matched_items': matched,
            'unmatched_items': total - matched,
            'match_rate': (matched / total) * 100,
            'passes_threshold': matched / total >= 0.80,
            'match_types': match_types
        }
    
    def generate_report(self, results: List[MatchResult], stats: Dict) -> str:
        """Generate a detailed test report"""
        report = []
        report.append("=" * 80)
        report.append("USDA FoodKeeper Shelf-Life Mapping Test Report")
        report.append("=" * 80)
        report.append(f"\nTest Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\nHypothesis: FoodKeeper provides mapping for at least 80% of tested items")
        
        report.append("\n" + "-" * 80)
        report.append("SUMMARY STATISTICS")
        report.append("-" * 80)
        report.append(f"Total Items Tested: {stats['total_items']}")
        report.append(f"Successfully Matched: {stats['matched_items']}")
        report.append(f"Unmatched: {stats['unmatched_items']}")
        report.append(f"Match Rate: {stats['match_rate']:.1f}%")
        report.append(f"\nResult: {'✓ PASS' if stats['passes_threshold'] else '✗ FAIL'}")
        report.append(f"Threshold: 80% | Achieved: {stats['match_rate']:.1f}%")
        
        report.append(f"\nMatch Type Breakdown:")
        for match_type, count in stats['match_types'].items():
            report.append(f"  - {match_type.capitalize()}: {count}")
        
        report.append("\n" + "-" * 80)
        report.append("SUCCESSFUL MATCHES")
        report.append("-" * 80)
        for result in results:
            if result.matched:
                shelf_life = result.shelf_life_data
                report.append(f"\n✓ {result.test_item}")
                report.append(f"  Matched: {result.foodkeeper_name} (ID: {result.foodkeeper_id})")
                report.append(f"  Match Type: {result.match_type}")
                if shelf_life:
                    if shelf_life.get('refrigerate'):
                        report.append(f"  Refrigerate: {shelf_life['refrigerate']}")
                    if shelf_life.get('freeze'):
                        report.append(f"  Freeze: {shelf_life['freeze']}")
                    if shelf_life.get('pantry'):
                        report.append(f"  Pantry: {shelf_life['pantry']}")
        
        if any(not r.matched for r in results):
            report.append("\n" + "-" * 80)
            report.append("UNMATCHED ITEMS")
            report.append("-" * 80)
            for result in results:
                if not result.matched:
                    report.append(f"✗ {result.test_item}")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)
    
    def save_results(self, results: List[MatchResult], stats: Dict, 
                     output_dir: str = "."):
        """Save results to JSON file"""
        output_path = Path(output_dir) / f"foodkeeper_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output_data = {
            'metadata': {
                'test_date': datetime.now().isoformat(),
                'hypothesis': 'FoodKeeper provides mapping for at least 80% of tested items',
                'threshold': 0.80
            },
            'statistics': stats,
            'results': [asdict(r) for r in results]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        return output_path


def main():
    """Main execution function"""
    # Configuration
    FOODKEEPER_JSON = "FoodKeeper.json"
    print("Initializing USDA FoodKeeper Test System...")
    print("=" * 80)
    
    try:
        # Initialize database
        db = FoodKeeperDB(FOODKEEPER_JSON)
        print(f"✓ Loaded FoodKeeper database")
        print(f"  Products indexed: {len(db.data.get('product_data', []))}")
        
        # Initialize test runner
        runner = TestRunner(db)
        print(f"✓ Created test suite with {len(runner.test_items)} items")
        
        # Run tests
        print("\nRunning tests...")
        results, stats = runner.run_tests()
        
        # Generate and display report
        report = runner.generate_report(results, stats)
        print("\n" + report)
        
        # Save results
        output_file = runner.save_results(results, stats)
        print(f"\n✓ Results saved to: {output_file}")
        
        # Exit with appropriate code
        return 0 if stats['passes_threshold'] else 1
        
    except FileNotFoundError:
        print(f"✗ Error: Could not find {FOODKEEPER_JSON}")
        print(f"  Please ensure the FoodKeeper JSON file is in the current directory")
        return 1
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())