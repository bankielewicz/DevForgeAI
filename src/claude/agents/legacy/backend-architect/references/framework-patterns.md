# Framework-Specific Patterns for Backend Architect

**Version**: 1.0 | **Status**: Reference | **Agent**: backend-architect

---

## Python (FastAPI + SQLAlchemy)

**Domain Entity:**
```python
class Order:
    def __init__(self, order_id: int, customer_id: int):
        self.id = order_id
        self.customer_id = customer_id
        self.items = []
```

**Application Service:**
```python
class OrderService:
    def __init__(self, order_repo: IOrderRepository):
        self.order_repo = order_repo

    def create_order(self, customer_id: int, items: List[OrderItemDTO]) -> OrderDTO:
        order = Order(customer_id=customer_id)
        for item_dto in items:
            order.add_item(item_dto.product_id, item_dto.quantity)
        self.order_repo.save(order)
        return OrderDTO.from_entity(order)
```

**Infrastructure Repository:**
```python
from sqlalchemy.orm import Session

class SqlAlchemyOrderRepository(IOrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, order: Order) -> None:
        order_model = OrderModel(
            id=order.id,
            customer_id=order.customer_id,
            status=order.status
        )
        self.session.add(order_model)
        self.session.commit()
```

**API Controller:**
```python
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/orders")
def create_order(
    request: CreateOrderRequest,
    order_service: OrderService = Depends(get_order_service)
) -> OrderResponse:
    order_dto = order_service.create_order(
        customer_id=request.customer_id,
        items=request.items
    )
    return OrderResponse.from_dto(order_dto)
```

---

## JavaScript/TypeScript (Node.js + Express)

**Domain Entity:**
```typescript
export class Order {
  private items: OrderItem[] = [];

  constructor(
    public readonly id: number,
    public readonly customerId: number
  ) {}

  addItem(product: Product, quantity: number): void {
    if (quantity <= 0) {
      throw new Error('Quantity must be positive');
    }
    this.items.push(new OrderItem(product, quantity));
  }

  calculateTotal(): number {
    return this.items.reduce((sum, item) => sum + item.getSubtotal(), 0);
  }
}
```

**Application Service:**
```typescript
export class OrderService {
  constructor(private orderRepository: IOrderRepository) {}

  async createOrder(customerId: number, items: OrderItemDTO[]): Promise<OrderDTO> {
    const order = new Order(0, customerId);
    for (const item of items) {
      order.addItem(item.product, item.quantity);
    }
    await this.orderRepository.save(order);
    return OrderDTO.fromEntity(order);
  }
}
```

**Infrastructure Repository:**
```typescript
export class TypeOrmOrderRepository implements IOrderRepository {
  constructor(private repository: Repository<OrderEntity>) {}

  async save(order: Order): Promise<void> {
    const entity = new OrderEntity();
    entity.customerId = order.customerId;
    entity.status = order.status;
    await this.repository.save(entity);
  }
}
```

---

## C# (.NET Core)

**Domain Entity:**
```csharp
public class Order
{
    public int Id { get; private set; }
    public int CustomerId { get; private set; }
    private List<OrderItem> _items = new();
    public IReadOnlyCollection<OrderItem> Items => _items.AsReadOnly();

    public Order(int customerId) { CustomerId = customerId; }

    public void AddItem(Product product, int quantity)
    {
        if (quantity <= 0) throw new ArgumentException("Quantity must be positive");
        _items.Add(new OrderItem(product, quantity));
    }

    public decimal CalculateTotal() => _items.Sum(item => item.GetSubtotal());
}
```

**Application Service:**
```csharp
public class OrderService
{
    private readonly IOrderRepository _orderRepository;
    public OrderService(IOrderRepository orderRepository) { _orderRepository = orderRepository; }

    public async Task<OrderDTO> CreateOrderAsync(int customerId, List<OrderItemDTO> items)
    {
        var order = new Order(customerId);
        foreach (var item in items) { order.AddItem(item.Product, item.Quantity); }
        await _orderRepository.SaveAsync(order);
        return OrderDTO.FromEntity(order);
    }
}
```

---

## Database Transactions

**Python (SQLAlchemy):**
```python
def create_order_with_payment(self, order_data, payment_data):
    with self.session.begin():
        order = self.order_repo.save(order_data)
        payment = self.payment_repo.save(payment_data)
        return order, payment
```

**JavaScript (TypeORM):**
```typescript
async createOrderWithPayment(orderData, paymentData) {
  return await this.connection.transaction(async manager => {
    const order = await manager.save(Order, orderData);
    const payment = await manager.save(Payment, paymentData);
    return { order, payment };
  });
}
```

## Input Validation

```python
def create_order(self, request: CreateOrderRequest) -> OrderDTO:
    if not request.customer_id:
        raise ValueError("Customer ID is required")
    if not request.items:
        raise ValueError("Order must have at least one item")
    order = Order(customer_id=request.customer_id)
    # ...
```
