import time
import random

# --- Simulated API Service Definitions ---

class APIError(Exception):
    """Base exception for simulated API errors."""
    pass

class StockError(APIError):
    """Raised when stock check fails."""
    pass

class PaymentError(APIError):
    """Raised when payment processing fails."""
    pass

class OrderCreationError(APIError):
    """Raised when order creation fails."""
    pass

class EmailError(APIError):
    """Raised when sending confirmation email fails."""
    pass

def _simulate_api_call(api_name, min_delay=0.1, max_delay=0.5, success_rate=0.9):
    """Helper to simulate API latency and potential failure."""
    time.sleep(random.uniform(min_delay, max_delay))
    if random.random() > success_rate:
        print(f"  [API] {api_name} FAILED (simulated error).")
        return False # Indicate failure
    print(f"  [API] {api_name} successful.")
    return True # Indicate success

def check_stock(product_id, quantity):
    """Simulates checking product stock via an external API."""
    print(f"Checking stock for product {product_id}, quantity {quantity}...")
    if not _simulate_api_call("Stock Check API", success_rate=0.8):
        raise StockError(f"Not enough stock for product {product_id} or API unavailable.")
    # Simulate specific business logic for product PROD002
    if product_id == "PROD002" and quantity > 1:
        raise StockError(f"Only 1 unit of {product_id} available in stock.")
    return True

def process_payment(user_id, amount):
    """Simulates processing a payment via a payment gateway API."""
    print(f"Processing payment for user {user_id}, amount ${amount:.2f}...")
    if not _simulate_api_call("Payment Gateway API", success_rate=0.9):
        raise PaymentError(f"Payment failed for user {user_id}.")
    transaction_id = f"TXN-{random.randint(10000, 99999)}"
    return transaction_id

def create_order(user_id, product_id, quantity, transaction_id):
    """Simulates creating an order in the order management system API."""
    print(f"Creating order for user {user_id}, product {product_id}, quantity {quantity} with transaction {transaction_id}...")
    if not _simulate_api_call("Order Service API", success_rate=0.95):
        raise OrderCreationError(f"Failed to create order for user {user_id}.")
    order_id = f"ORD-{random.randint(1000, 9999)}"
    return order_id

def send_confirmation_email(user_id, order_id):
    """Simulates sending an order confirmation email via an email service API."""
    print(f"Sending confirmation email to user {user_id} for order {order_id}...")
    if not _simulate_api_call("Email Service API", success_rate=0.7): # Email service can be flaky
        raise EmailError(f"Failed to send confirmation email for order {order_id}.")
    return True

# --- API Orchestration Logic ---

def orchestrate_ecommerce_order(user_id, product_id, quantity, payment_amount):
    """
    Orchestrates a complex e-commerce order workflow involving multiple API calls.
    This function demonstrates sequential execution, conditional logic, and error handling
    across different simulated services, which is the core concept of API orchestration.
    """
    print(f"\n--- Starting Order Orchestration for User: {user_id}, Product: {product_id} ---")
    order_id = None
    transaction_id = None

    try:
        # Orchestration Step 1: Check product stock (critical pre-condition)
        # If this fails, the entire workflow stops as we cannot fulfill the order.
        print("Orchestrator: Attempting to check stock...")
        check_stock(product_id, quantity)
        print("Orchestrator: Stock check successful.")

        # Orchestration Step 2: Process payment
        # This is another critical step. If payment fails, we cannot proceed with order creation.
        print("Orchestrator: Attempting to process payment...")
        transaction_id = process_payment(user_id, payment_amount)
        print(f"Orchestrator: Payment successful, Transaction ID: {transaction_id}")

        # Orchestration Step 3: Create the order
        # This step depends on successful stock check and payment.
        print("Orchestrator: Attempting to create order...")
        order_id = create_order(user_id, product_id, quantity, transaction_id)
        print(f"Orchestrator: Order created successfully, Order ID: {order_id}")

        # Orchestration Step 4: Send confirmation email (post-order, less critical)
        # This step is important but its failure should generally NOT revert the order.
        # It can be retried or handled asynchronously later, demonstrating fault tolerance.
        print("Orchestrator: Attempting to send confirmation email...")
        try:
            send_confirmation_email(user_id, order_id)
            print("Orchestrator: Confirmation email sent successfully.")
        except EmailError as e:
            print(f"Orchestrator: WARNING - Failed to send confirmation email: {e}. Order {order_id} is still valid.")
            # In a real system, this would be logged for a retry mechanism or manual intervention.

        print(f"\n--- Order Orchestration COMPLETE for User: {user_id}, Order ID: {order_id} ---")
        return True

    except StockError as e:
        print(f"Orchestrator: ERROR - Stock check failed: {e}. Order aborted.")
    except PaymentError as e:
        print(f"Orchestrator: ERROR - Payment failed: {e}. Order aborted.")
    except OrderCreationError as e:
        print(f"Orchestrator: ERROR - Order creation failed: {e}. Attempting to refund payment if possible...")
        # This demonstrates a compensation action: if order creation fails after payment, attempt refund.
        if transaction_id:
            print(f"  (Simulated) Initiating refund for transaction {transaction_id}...")
            # In a real system, a refund_payment(transaction_id) API call would be made here.
        else:
            print("  No transaction ID available for refund.")
    except APIError as e:
        print(f"Orchestrator: An unexpected API error occurred: {e}. Order aborted.")
    except Exception as e:
        print(f"Orchestrator: An unhandled error occurred during orchestration: {e}. Order aborted.")

    print(f"\n--- Order Orchestration FAILED for User: {user_id} ---")
    return False

# --- Main Execution Block ---

if __name__ == "__main__":
    print("This example demonstrates API orchestration for an e-commerce order workflow.")
    print("Each 'API call' is simulated with a random delay and a chance of failure.")
    print("The orchestrator coordinates these calls, handles errors, and performs conditional logic.")
    print("Run the script multiple times to observe different failure scenarios due to randomness.")

    # Scenario 1: Successful order
    print("\n==================================================")
    print("Running Scenario 1: Attempting a successful order")
    print("==================================================")
    orchestrate_ecommerce_order("user123", "PROD001", 2, 49.99)

    # Scenario 2: Stock failure (due to specific business logic)
    print("\n==================================================")
    print("Running Scenario 2: Order fails due to insufficient stock")
    print("==================================================")
    orchestrate_ecommerce_order("user456", "PROD002", 2, 29.99) # PROD002 only has 1 unit available

    # Scenario 3: Payment failure (due to simulation randomness)
    print("\n==================================================")
    print("Running Scenario 3: Order fails due to payment processing error")
    print("  (May require multiple runs to hit the random failure)")
    print("==================================================")
    orchestrate_ecommerce_order("user789", "PROD003", 1, 100.00)

    # Scenario 4: Order creation failure (due to simulation randomness) with refund attempt
    print("\n==================================================")
    print("Running Scenario 4: Order fails during creation, triggering refund")
    print("  (May require multiple runs to hit the random failure)")
    print("==================================================")
    orchestrate_ecommerce_order("user007", "PROD004", 3, 75.50)
