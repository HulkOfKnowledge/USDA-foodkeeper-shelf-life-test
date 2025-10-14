# USDA FoodKeeper Shelf Life Test


## 🎯 Hypothesis

We believe that expiration dates for fresh food produce can be estimated using the open-source USDA FoodKeeper database.

**Success Criteria:** FoodKeeper provides mapping for at least 80% of tested food items.

## 📊 Test Results

The system tests **50 diverse food items** across major categories:
- Dairy Products & Eggs
- Meat & Poultry
- Seafood
- Fresh Produce (Fruits & Vegetables)
- Baked Goods
- Frozen Foods
- Condiments
- Beverages
- Pantry Staples

## 🚀 Quick Start

### Prerequisites

- Python 3.7+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/HulkOfKnowledge/USDA-foodkeeper-shelf-life-test.git
cd USDA-foodkeeper-shelf-life-test
```

2. Run the test:
```bash
python test_shelf_life.py
```

## 📖 Usage

### Basic Usage

Simply run the script with the FoodKeeper JSON file in the same directory:

```bash
python test_foodkeeper.py
```

### Output

The script generates:
1. **Console Report**: Detailed test results with statistics
2. **JSON Export**: Timestamped file with complete test data (`foodkeeper_test_results_YYYYMMDD_HHMMSS.json`)

### Sample Output

```
================================================================================
USDA FoodKeeper Shelf-Life Mapping Test Report
================================================================================

Test Date: 2025-10-14 10:30:45

--------------------------------------------------------------------------------
SUMMARY STATISTICS
--------------------------------------------------------------------------------
Total Items Tested: 50
Successfully Matched: 45
Unmatched: 5
Match Rate: 90.0%

Result: ✓ PASS
Threshold: 80% | Achieved: 90.0%

Match Type Breakdown:
  - Exact: 30
  - Keyword: 10
  - Fuzzy: 5
```

## 🔧 Features

### Matching Strategies

1. **Exact Match**: Direct name lookup in the database
2. **Keyword Match**: Searches using product keywords field
3. **Fuzzy Match**: Partial string matching for flexibility
4. **Variant Support**: Tests multiple search terms per item

### Comprehensive Data Extraction

For each matched item, the system extracts:
- Refrigeration shelf life
- Freezer shelf life
- Pantry shelf life
- Product category and subcategory

## 📁 Project Structure

```
USDA-foodkeeper-shelf-life-test/
├── test_shelf_life.py          # Main test script
├── FoodKeeper.json             # USDA database
├── README.md                   # This file
```

## 🧪 Test Suite

The test suite includes 50 carefully selected items representing typical grocery shopping:

**Dairy** (5 items): milk, cheddar cheese, yogurt, butter, eggs

**Meat** (5 items): chicken breast, ground beef, bacon, pork chops, steak

**Produce** (14 items): lettuce, tomatoes, carrots, broccoli, spinach, onions, potatoes, bell peppers, apples, bananas, oranges, strawberries, grapes, blueberries

**Seafood** (5 items): salmon, shrimp, tuna, cod, lobster

**Other Categories** (21 items): bread, bagels, muffins, ice cream, frozen pizza, ketchup, mayonnaise, mustard, orange juice, deli ham, turkey slices, salami, rice, pasta, flour, sugar, cooking oil, and more

## 🔬 Methodology

The testing process follows these steps:

1. **Database Loading**: Parse and index the USDA FoodKeeper JSON
2. **Search Index Building**: Create lookup tables for efficient searching
3. **Test Execution**: Search for each test item using multiple strategies
4. **Result Analysis**: Calculate match rates and statistics
5. **Report Generation**: Create results json

## 📊 Data Source

This project uses the **USDA FoodKeeper Database**, a trusted government resource for food storage guidelines.

- **Source**: U.S. Department of Agriculture (USDA)
- **Maintained by**: Food Safety and Inspection Service (FSIS)
- **License**: Public Domain (U.S. Government Work)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The USDA FoodKeeper data is in the public domain as a U.S. Government work.


## 🔗 Resources

- [FoodKeeper App](https://www.foodsafety.gov/keep-food-safe/foodkeeper-app)
- [USDA Food Safety](https://www.fsis.usda.gov/)
- [FoodSafety.gov](https://www.foodsafety.gov/)
- [FoodKeeper Json](https://www.foodsafety.gov/sites/default/files/foodkeeper_data_url_en.json)

---
