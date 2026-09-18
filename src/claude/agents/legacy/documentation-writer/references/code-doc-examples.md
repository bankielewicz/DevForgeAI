# Documentation Writer - Code Documentation Examples

## JavaScript/TypeScript (JSDoc)

```typescript
/**
 * Calculates the total price including tax
 *
 * @param {number} basePrice - The base price before tax
 * @param {number} taxRate - The tax rate as a decimal (e.g., 0.08 for 8%)
 * @returns {number} The total price including tax
 * @throws {Error} If basePrice or taxRate are negative
 *
 * @example
 * const total = calculateTotalPrice(100, 0.08);
 * console.log(total); // 108
 */
function calculateTotalPrice(basePrice: number, taxRate: number): number {
  if (basePrice < 0 || taxRate < 0) {
    throw new Error('Price and tax rate must be non-negative');
  }
  return basePrice * (1 + taxRate);
}
```

## Python (Docstrings)

```python
def calculate_total_price(base_price: float, tax_rate: float) -> float:
    """
    Calculate the total price including tax.

    Args:
        base_price: The base price before tax
        tax_rate: The tax rate as a decimal (e.g., 0.08 for 8%)

    Returns:
        The total price including tax

    Raises:
        ValueError: If base_price or tax_rate are negative

    Example:
        >>> calculate_total_price(100, 0.08)
        108.0
    """
    if base_price < 0 or tax_rate < 0:
        raise ValueError('Price and tax rate must be non-negative')
    return base_price * (1 + tax_rate)
```

## C# (XML Documentation)

```csharp
/// <summary>
/// Calculates the total price including tax
/// </summary>
/// <param name="basePrice">The base price before tax</param>
/// <param name="taxRate">The tax rate as a decimal (e.g., 0.08 for 8%)</param>
/// <returns>The total price including tax</returns>
/// <exception cref="ArgumentException">
/// Thrown when basePrice or taxRate are negative
/// </exception>
/// <example>
/// <code>
/// decimal total = CalculateTotalPrice(100m, 0.08m);
/// Console.WriteLine(total); // 108
/// </code>
/// </example>
public decimal CalculateTotalPrice(decimal basePrice, decimal taxRate)
{
    if (basePrice < 0 || taxRate < 0)
    {
        throw new ArgumentException("Price and tax rate must be non-negative");
    }
    return basePrice * (1 + taxRate);
}
```
