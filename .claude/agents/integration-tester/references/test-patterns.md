# Integration Test Patterns

**Purpose:** Complete code examples for API contract testing, database transactions, external service mocking, component interactions, and E2E user journeys.

---

## API Contract Testing

**Test Structure (JavaScript):**
```javascript
describe('POST /api/users', () => {
  it('should create user with valid data', async () => {
    // Arrange
    const userData = {
      email: 'test@example.com',
      password: 'SecurePass123!',
      name: 'Test User'
    };

    // Act
    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(201);

    // Assert - Response structure
    expect(response.body).toHaveProperty('id');
    expect(response.body).toHaveProperty('email', userData.email);
    expect(response.body).toHaveProperty('name', userData.name);
    expect(response.body).not.toHaveProperty('password');

    // Assert - Database state
    const user = await db.users.findById(response.body.id);
    expect(user).toBeDefined();
    expect(user.email).toBe(userData.email);
  });

  it('should reject invalid email', async () => {
    const userData = {
      email: 'invalid-email',
      password: 'SecurePass123!',
      name: 'Test User'
    };

    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(400);

    expect(response.body).toHaveProperty('error');
    expect(response.body.error).toContain('email');
  });

  it('should reject duplicate email', async () => {
    await createUser({ email: 'test@example.com' });

    const userData = {
      email: 'test@example.com',
      password: 'SecurePass123!',
      name: 'Another User'
    };

    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(409);

    expect(response.body.error).toContain('already exists');
  });
});
```

---

## Database Transaction Testing

**Python Example:**
```python
def test_create_order_transaction():
    """Test that order creation is atomic"""
    user = create_test_user()
    product = create_test_product(stock=10)

    order = create_order(user.id, [
        {'product_id': product.id, 'quantity': 5}
    ])

    assert order.id is not None
    assert order.user_id == user.id

    updated_product = Product.query.get(product.id)
    assert updated_product.stock == 5

    assert len(order.items) == 1
    assert order.items[0].product_id == product.id
    assert order.items[0].quantity == 5


def test_create_order_rollback_on_error():
    """Test that transaction rolls back on error"""
    user = create_test_user()
    product = create_test_product(stock=10)

    with pytest.raises(InsufficientStockError):
        create_order(user.id, [
            {'product_id': product.id, 'quantity': 15}
        ])

    orders = Order.query.filter_by(user_id=user.id).all()
    assert len(orders) == 0

    updated_product = Product.query.get(product.id)
    assert updated_product.stock == 10
```

---

## External Service Mocking

**JavaScript with Nock:**
```javascript
const nock = require('nock');

describe('Payment Processing', () => {
  afterEach(() => {
    nock.cleanAll();
  });

  it('should process successful payment', async () => {
    const paymentMock = nock('https://api.stripe.com')
      .post('/v1/charges')
      .reply(200, {
        id: 'ch_123456',
        status: 'succeeded',
        amount: 5000
      });

    const result = await processPayment({
      amount: 5000,
      currency: 'usd',
      source: 'tok_visa'
    });

    expect(result.success).toBe(true);
    expect(result.transactionId).toBe('ch_123456');
    expect(paymentMock.isDone()).toBe(true);
  });

  it('should handle payment failure', async () => {
    nock('https://api.stripe.com')
      .post('/v1/charges')
      .reply(402, {
        error: {
          code: 'card_declined',
          message: 'Your card was declined'
        }
      });

    const result = await processPayment({
      amount: 5000,
      currency: 'usd',
      source: 'tok_chargeDeclined'
    });

    expect(result.success).toBe(false);
    expect(result.error).toContain('declined');
  });
});
```

---

## Component Interaction Testing

**C# Example:**
```csharp
[Fact]
public async Task CreateOrder_Should_UpdateInventory_And_SendNotification()
{
    var orderService = new OrderService(_dbContext, _inventoryService, _notificationService);
    var userId = await CreateTestUser();
    var productId = await CreateTestProduct(stock: 10);

    var order = await orderService.CreateOrderAsync(userId, new[]
    {
        new OrderItem { ProductId = productId, Quantity = 2 }
    });

    Assert.NotNull(order);
    Assert.Equal(userId, order.UserId);

    var product = await _dbContext.Products.FindAsync(productId);
    Assert.Equal(8, product.Stock);

    var notifications = await _dbContext.Notifications
        .Where(n => n.UserId == userId)
        .ToListAsync();
    Assert.Single(notifications);
    Assert.Contains("Order created", notifications[0].Message);
}
```

---

## End-to-End User Journey

**Full workflow test (JavaScript):**
```javascript
describe('E2E: User Registration to Purchase', () => {
  it('should complete full user journey', async () => {
    // Step 1: Register user
    const registerResponse = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'buyer@example.com',
        password: 'SecurePass123!',
        name: 'Test Buyer'
      })
      .expect(201);

    const userId = registerResponse.body.id;

    // Step 2: Login
    const loginResponse = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'buyer@example.com',
        password: 'SecurePass123!'
      })
      .expect(200);

    const token = loginResponse.body.token;

    // Step 3: Browse products
    const productsResponse = await request(app)
      .get('/api/products')
      .set('Authorization', `Bearer ${token}`)
      .expect(200);

    expect(productsResponse.body.length).toBeGreaterThan(0);
    const productId = productsResponse.body[0].id;

    // Step 4: Add to cart
    await request(app)
      .post('/api/cart/items')
      .set('Authorization', `Bearer ${token}`)
      .send({ productId, quantity: 1 })
      .expect(201);

    // Step 5: Create order
    const orderResponse = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${token}`)
      .send({ cartId: 'current' })
      .expect(201);

    expect(orderResponse.body).toHaveProperty('id');
    expect(orderResponse.body.items).toHaveLength(1);

    // Step 6: Verify order in database
    const order = await db.orders.findById(orderResponse.body.id);
    expect(order.userId).toBe(userId);
    expect(order.status).toBe('pending');
  });
});
```

---

## Test Fixtures and Setup

### Database Test Setup (JavaScript - Jest)
```javascript
beforeEach(async () => {
  await db.users.deleteMany({});
  await db.products.deleteMany({});
  await db.orders.deleteMany({});

  testUser = await db.users.create({
    email: 'test@example.com',
    name: 'Test User'
  });

  testProduct = await db.products.create({
    name: 'Test Product',
    price: 19.99,
    stock: 100
  });
});

afterEach(async () => {
  await db.connection.close();
});
```

### Docker Test Setup (Python - Pytest)
```python
@pytest.fixture(scope='session')
def docker_db():
    """Start PostgreSQL in Docker for testing"""
    container = docker.from_env().containers.run(
        'postgres:15-alpine',
        environment={
            'POSTGRES_DB': 'test_db',
            'POSTGRES_USER': 'test_user',
            'POSTGRES_PASSWORD': 'test_pass'
        },
        ports={'5432/tcp': 5433},
        detach=True,
        remove=True
    )
    time.sleep(5)
    yield 'postgresql://test_user:test_pass@localhost:5433/test_db'
    container.stop()


@pytest.fixture
def db_session(docker_db):
    """Provide database session for tests"""
    engine = create_engine(docker_db)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)
```
