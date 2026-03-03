"""
Test fixtures for code-quality-auditor testing (STORY-063)

Provides sample code files with known quality metrics for deterministic testing.
"""

import json
from pathlib import Path


# ============================================================================
# Sample Code: Extreme Complexity
# ============================================================================

PYTHON_EXTREME_COMPLEXITY = """
def process_order(order):
    '''
    Process order with extreme cyclomatic complexity: 28

    This function intentionally violates complexity threshold for testing.
    Real implementation should be refactored using Extract Method pattern.
    '''
    if order is None:
        return None
    if not order.items:
        return {"error": "No items"}
    if order.customer is None:
        return {"error": "No customer"}
    if order.total < 0:
        return {"error": "Invalid total"}

    if order.status == "pending":
        if order.payment_method == "credit_card":
            if order.card_valid:
                if order.balance >= order.total:
                    if order.cvv_match:
                        charge_card()
                    else:
                        request_cvv()
                else:
                    decline_payment()
            else:
                request_new_card()
        elif order.payment_method == "paypal":
            if order.paypal_verified:
                if order.paypal_balance >= order.total:
                    process_paypal()
                else:
                    request_paypal_topup()
            else:
                verify_paypal()
        elif order.payment_method == "cash":
            mark_cash_payment()
        elif order.payment_method == "bitcoin":
            if order.wallet_verified:
                process_crypto()
            else:
                verify_wallet()
        else:
            return {"error": "Invalid payment method"}
    elif order.status == "processing":
        if order.shipped:
            if order.tracking_available:
                update_tracking()
            else:
                request_tracking()
        else:
            prepare_shipment()
    elif order.status == "complete":
        archive_order()
    elif order.status == "cancelled":
        refund_payment()
    else:
        return {"error": "Invalid status"}

    return {"success": True}
"""

CSHARP_EXTREME_COMPLEXITY = """
public class OrderProcessor
{
    public OrderResult ProcessOrder(Order order)
    {
        // Cyclomatic complexity: 28
        if (order == null)
            return OrderResult.Null;

        if (order.Items == null || order.Items.Count == 0)
            return OrderResult.NoItems;

        if (order.Customer == null)
            return OrderResult.NoCustomer;

        if (order.Total < 0)
            return OrderResult.InvalidTotal;

        if (order.Status == OrderStatus.Pending)
        {
            if (order.PaymentMethod == PaymentMethod.CreditCard)
            {
                if (order.CardValid)
                {
                    if (order.Balance >= order.Total)
                    {
                        if (order.CvvMatch)
                            ChargeCard();
                        else
                            RequestCvv();
                    }
                    else
                        DeclinePayment();
                }
                else
                    RequestNewCard();
            }
            else if (order.PaymentMethod == PaymentMethod.PayPal)
            {
                if (order.PayPalVerified)
                {
                    if (order.PayPalBalance >= order.Total)
                        ProcessPayPal();
                    else
                        RequestPayPalTopup();
                }
                else
                    VerifyPayPal();
            }
            else if (order.PaymentMethod == PaymentMethod.Cash)
                MarkCashPayment();
            else if (order.PaymentMethod == PaymentMethod.Bitcoin)
            {
                if (order.WalletVerified)
                    ProcessCrypto();
                else
                    VerifyWallet();
            }
            else
                return OrderResult.InvalidPaymentMethod;
        }
        else if (order.Status == OrderStatus.Processing)
        {
            if (order.Shipped)
            {
                if (order.TrackingAvailable)
                    UpdateTracking();
                else
                    RequestTracking();
            }
            else
                PrepareShipment();
        }
        else if (order.Status == OrderStatus.Complete)
            ArchiveOrder();
        else if (order.Status == OrderStatus.Cancelled)
            RefundPayment();
        else
            return OrderResult.InvalidStatus;

        return OrderResult.Success;
    }
}
"""


# ============================================================================
# Sample Code: Extreme Duplication (>25%)
# ============================================================================

CODE_WITH_DUPLICATION = {
    "ServiceA.cs": """
public class ServiceA
{
    public void ValidateInput(string input)
    {
        // Duplicated validation logic (23 lines)
        if (string.IsNullOrEmpty(input))
            throw new ArgumentException("Input cannot be null or empty");

        if (input.Length > 100)
            throw new ArgumentException("Input too long");

        if (!Regex.IsMatch(input, @"^[a-zA-Z0-9]+$"))
            throw new ArgumentException("Invalid characters");

        if (input.Contains("  "))
            throw new ArgumentException("Double spaces not allowed");

        var trimmed = input.Trim();
        if (trimmed != input)
            throw new ArgumentException("Leading/trailing whitespace");

        if (char.IsDigit(input[0]))
            throw new ArgumentException("Cannot start with digit");
    }
}
""",
    "ServiceB.cs": """
public class ServiceB
{
    public void CheckData(string data)
    {
        // EXACT duplicate of validation logic (23 lines)
        if (string.IsNullOrEmpty(data))
            throw new ArgumentException("Input cannot be null or empty");

        if (data.Length > 100)
            throw new ArgumentException("Input too long");

        if (!Regex.IsMatch(data, @"^[a-zA-Z0-9]+$"))
            throw new ArgumentException("Invalid characters");

        if (data.Contains("  "))
            throw new ArgumentException("Double spaces not allowed");

        var trimmed = data.Trim();
        if (trimmed != data)
            throw new ArgumentException("Leading/trailing whitespace");

        if (char.IsDigit(data[0]))
            throw new ArgumentException("Cannot start with digit");
    }
}
"""
}


# ============================================================================
# Sample Code: Low Maintainability Index (<40)
# ============================================================================

PYTHON_LOW_MAINTAINABILITY = """
import math
import logging
from typing import List, Dict, Any

class LegacyDataProcessor:
    '''
    Legacy data processor with low maintainability index (~35)

    Issues:
    - 200+ lines in single file
    - High cyclomatic complexity
    - Poor naming
    - Nested logic
    - No separation of concerns
    '''

    def __init__(self):
        self.data = []
        self.results = {}
        self.errors = []
        self.cache = {}
        self.config = {}

    def process_all_data(self, input_data, config=None):
        if not input_data:
            return None

        if config:
            self.config = config

        # 50+ lines of complex processing logic
        for item in input_data:
            if not self._validate(item):
                self.errors.append(item)
                continue

            if self._check_cache(item):
                result = self.cache[item['id']]
            else:
                result = self._complex_calculation(item)
                self.cache[item['id']] = result

            self.results[item['id']] = result

        return self._aggregate_results()

    def _validate(self, item):
        # Complex validation with nested conditions
        if not item:
            return False
        if 'id' not in item:
            return False
        if 'data' not in item:
            return False
        # ... 20+ more validation checks
        return True

    def _check_cache(self, item):
        return item['id'] in self.cache

    def _complex_calculation(self, item):
        # 100+ lines of complex math and business logic
        # High cyclomatic complexity (20+)
        # Poor variable names (a, b, c, tmp, x, y)
        a = item['data']
        b = 0
        c = 0

        for x in a:
            if x > 0:
                if x % 2 == 0:
                    b += x * 2
                else:
                    b += x * 3
            else:
                if x % 2 == 0:
                    c -= x / 2
                else:
                    c -= x / 3

        tmp = math.sqrt(abs(b - c))
        return tmp * 1.5

    def _aggregate_results(self):
        # Another 50+ lines of aggregation logic
        total = 0
        for value in self.results.values():
            total += value
        return total
"""


# ============================================================================
# Mock Analysis Tool Outputs
# ============================================================================

MOCK_RADON_COMPLEXITY_OUTPUT = json.dumps([
    {
        "type": "method",
        "name": "process_order",
        "lineno": 2,
        "col": 0,
        "endline": 65,
        "complexity": 28,
        "rank": "F",
        "classname": None
    },
    {
        "type": "method",
        "name": "validate_input",
        "lineno": 68,
        "col": 0,
        "endline": 75,
        "complexity": 3,
        "rank": "A",
        "classname": None
    }
])

MOCK_RADON_MI_OUTPUT = json.dumps({
    "src/services.py": {
        "mi": 72.4,
        "rank": "A"
    },
    "src/legacy_processor.py": {
        "mi": 35.2,
        "rank": "C"
    }
})

MOCK_JSCPD_DUPLICATION_OUTPUT = json.dumps({
    "statistics": {
        "total": {
            "sources": 2,
            "lines": 2000,
            "tokens": 15000,
            "duplicatedLines": 540,
            "duplicatedTokens": 4050,
            "percentage": 27.0
        }
    },
    "duplicates": [
        {
            "format": "csharp",
            "lines": 23,
            "fragment": "validation logic",
            "firstFile": {
                "name": "src/ServiceA.cs",
                "start": 45,
                "end": 67
            },
            "secondFile": {
                "name": "src/ServiceB.cs",
                "start": 123,
                "end": 145
            }
        }
    ]
})


# ============================================================================
# Expected Analysis Results
# ============================================================================

EXPECTED_COMPLEXITY_VIOLATION = {
    "type": "complexity",
    "severity": "CRITICAL",
    "function": "process_order",
    "score": 28,
    "threshold": 20,
    "file": "src/services.py",
    "line": 2,
    "business_impact": (
        "40% higher defect rate compared to functions with complexity <10. "
        "Requires 28+ test cases for full coverage. "
        "3x longer onboarding time for new developers."
    ),
    "refactoring_pattern": (
        "Extract Method: Split process_order() into 5 methods:\n"
        "1. ValidateOrder() - complexity <6\n"
        "2. CalculateTotal() - complexity <6\n"
        "3. ProcessPayment() - complexity <6\n"
        "4. PrepareShipment() - complexity <6\n"
        "5. UpdateStatus() - complexity <6\n\n"
        "Target: Each method complexity <6 (current: 28 → goal: excellent)"
    )
}

EXPECTED_DUPLICATION_VIOLATION = {
    "type": "duplication",
    "severity": "CRITICAL",
    "percentage": 27.0,
    "threshold": 25.0,
    "duplicate_blocks": [
        {
            "files": ["src/ServiceA.cs:45-67", "src/ServiceB.cs:123-145"],
            "lines": 23,
            "pattern": "validation logic"
        }
    ],
    "business_impact": (
        "Changes must be replicated in 2+ places (bug multiplication risk). "
        "27% of codebase is redundant (wasted maintenance effort). "
        "Violates DRY principle - refactoring required."
    ),
    "refactoring_pattern": (
        "Extract to Shared Utility Class:\n"
        "1. Create ValidationService in src/Common/Utilities/\n"
        "2. Extract ValidateInput() method (23 lines)\n"
        "3. Replace duplicate code in ServiceA and ServiceB with ValidationService.ValidateInput()\n"
        "4. Add unit tests for ValidationService\n\n"
        "Target: Reduce duplication from 27% to <20% (acceptable range)"
    )
}

EXPECTED_MAINTAINABILITY_VIOLATION = {
    "type": "maintainability",
    "severity": "CRITICAL",
    "file": "src/legacy_processor.py",
    "mi": 35.2,
    "threshold": 40,
    "business_impact": (
        "50% slower code modifications compared to MI >70. "
        "3x higher bug introduction risk during changes. "
        "Team morale impact: developers avoid working in this file."
    ),
    "refactoring_pattern": (
        "Simplify Logic and Extract Methods:\n"
        "1. Extract _validate() method into separate Validator class\n"
        "2. Extract _complex_calculation() into CalculationService\n"
        "3. Reduce file size from 200+ lines to <100 lines per class\n"
        "4. Improve variable naming (a, b, c → meaningful names)\n"
        "5. Reduce cyclomatic complexity per method to <10\n\n"
        "Target: Increase MI from 35.2 to >50 (acceptable range)"
    )
}


# ============================================================================
# Utility Functions
# ============================================================================

def create_test_source_file(temp_dir: Path, filename: str, content: str) -> Path:
    """
    Create a test source file with given content.

    Args:
        temp_dir: Temporary directory path
        filename: Name of file to create
        content: File content

    Returns:
        Path to created file
    """
    src_dir = temp_dir / "src"
    src_dir.mkdir(parents=True, exist_ok=True)

    file_path = src_dir / filename
    file_path.write_text(content)

    return file_path


def create_test_context_files(temp_dir: Path, language: str = "Python") -> dict:
    """
    Create test context files (tech-stack.md, quality-metrics.md).

    Args:
        temp_dir: Temporary directory path
        language: Programming language (Python, C#, Node.js, etc.)

    Returns:
        Dict with file paths
    """
    context_dir = temp_dir / "devforgeai" / "context"
    context_dir.mkdir(parents=True, exist_ok=True)

    qa_dir = temp_dir / "devforgeai" / "qa"
    qa_dir.mkdir(parents=True, exist_ok=True)

    # tech-stack.md
    tech_stack = context_dir / "tech-stack.md"
    tech_stack.write_text(f"""# Tech Stack

## Backend
- Language: {language}

## Testing
- Framework: pytest
""")

    # quality-metrics.md
    quality_metrics = qa_dir / "quality-metrics.md"
    quality_metrics.write_text("""# Quality Metrics

## Code Quality Thresholds

### Cyclomatic Complexity
- CRITICAL: >20
- WARNING: 15-20
- ACCEPTABLE: <15

### Code Duplication
- CRITICAL: >25%
- WARNING: 20-25%
- ACCEPTABLE: <20%

### Maintainability Index
- CRITICAL: <40
- WARNING: 40-50
- ACCEPTABLE: >50
""")

    return {
        "tech_stack": tech_stack,
        "quality_metrics": quality_metrics
    }
