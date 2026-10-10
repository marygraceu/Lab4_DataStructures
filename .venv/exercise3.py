# ADDITIONAL EXERCISE NO. 3: TRANSACTION HISTORY ANALYZER
# Student-specific inputs required by the worksheet
LAST_NAME = "PENA"
SEED_NUM = 8
FAVORITE_ARTIST = "LANY"

from collections import defaultdict

# Five common products with fixed prices
PRODUCT_PRICES = {
    "NOTEBOOK": 45.00,
    "PEN": 12.00,
    "USB": 250.00,
    "HEADPHONES": 550.00,
    "CALCULATOR": 350.00,
}
PRODUCTS = list(PRODUCT_PRICES)
CUSTOMERS = [f"{LAST_NAME}_C{i}" for i in range(1, 6)]


def generate_quantity(product_index, customer_index, character_position):
    """Generate a positive quantity based on SEED_NUM and artist character positions."""
    artist_value = ord(FAVORITE_ARTIST[character_position % len(FAVORITE_ARTIST)])
    return ((SEED_NUM + artist_value + product_index + customer_index) % 5) + 1


def generate_transactions():
    """Create transactions for five customers and include a repeated purchase."""
    records = []
    transaction_number = 1

    for customer_index, customer in enumerate(CUSTOMERS):
        for product_index in range(3):
            product = PRODUCTS[(customer_index + product_index) % len(PRODUCTS)]
            quantity = generate_quantity(
                product_index, customer_index, customer_index + product_index
            )
            unit_price = PRODUCT_PRICES[product]
            records.append({
                "transaction_id": f"T{transaction_number:03d}",
                "customer": customer,
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "transaction_value": quantity * unit_price,
            })
            transaction_number += 1

    # Required repeated customer-product transaction
    repeated_record = records[0].copy()
    repeated_record["transaction_id"] = f"T{transaction_number:03d}"
    records.append(repeated_record)
    return records


def print_section(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def main():
    transactions = generate_transactions()

    customer_summary = defaultdict(
        lambda: {"records": 0, "quantity": 0, "spending": 0.0, "products": set()}
    )
    product_summary = defaultdict(
        lambda: {"records": 0, "quantity": 0, "sales": 0.0, "customers": set()}
    )
    customer_product_counts = defaultdict(int)
    overall_value = 0.0
    overall_quantity = 0

    # Analyze the complete transaction dataset
    for record in transactions:
        customer = record["customer"]
        product = record["product"]
        quantity = record["quantity"]
        value = record["transaction_value"]

        customer_summary[customer]["records"] += 1
        customer_summary[customer]["quantity"] += quantity
        customer_summary[customer]["spending"] += value
        customer_summary[customer]["products"].add(product)

        product_summary[product]["records"] += 1
        product_summary[product]["quantity"] += quantity
        product_summary[product]["sales"] += value
        product_summary[product]["customers"].add(customer)

        customer_product_counts[(customer, product)] += 1
        overall_value += value
        overall_quantity += quantity

    repeated_purchases = [
        (customer, product, count)
        for (customer, product), count in customer_product_counts.items()
        if count > 1
    ]
    distinct_customers = sorted({record["customer"] for record in transactions})
    distinct_products = sorted({record["product"] for record in transactions})

    print_section("FINAL CONSOLIDATED TRANSACTION REPORT")
    print(f"Student: {LAST_NAME} | SEED_NUM: {SEED_NUM} | FAVORITE_ARTIST: {FAVORITE_ARTIST}")

    # Assessment Data 1: Generated Transaction Records
    print_section("1. GENERATED TRANSACTION RECORDS")
    print(f"{'ID':<7} {'CUSTOMER':<12} {'PRODUCT':<14} {'QUANTITY':>8}")
    print("-" * 48)
    for record in transactions:
        print(f"{record['transaction_id']:<7} {record['customer']:<12} "
              f"{record['product']:<14} {record['quantity']:>8}")

    # Assessment Data 2: Organized Transaction Data
    print_section("2. ORGANIZED TRANSACTION DATA")
    print(f"{'ID':<7} {'CUSTOMER':<12} {'PRODUCT':<14} {'QUANTITY':>8} "
          f"{'UNIT PRICE':>12} {'TRANSACTION VALUE':>19}")
    print("-" * 78)
    for record in transactions:
        print(f"{record['transaction_id']:<7} {record['customer']:<12} "
              f"{record['product']:<14} {record['quantity']:>8} "
              f"{record['unit_price']:>12.2f} {record['transaction_value']:>19.2f}")

    # Assessment Data 3: Repeated/Distinct Transactions
    print_section("3. REPEATED/DISTINCT TRANSACTIONS")
    print(f"Distinct customers: {len(distinct_customers)} ({', '.join(distinct_customers)})")
    print(f"Distinct products: {len(distinct_products)} ({', '.join(distinct_products)})")
    print("Repeated customer-product purchases:")
    if repeated_purchases:
        for customer, product, count in sorted(repeated_purchases):
            print(f"- {customer} / {product}: {count} transaction records")
    else:
        print("- None")

    # Assessment Data 4: Transaction Values
    print_section("4. TRANSACTION VALUES")
    for record in transactions:
        print(f"{record['transaction_id']}: {record['quantity']} x "
              f"{record['product']} at {record['unit_price']:.2f} = "
              f"{record['transaction_value']:.2f}")
    print(f"Overall transaction value: {overall_value:.2f}")

    # Assessment Data 5: Customer Summaries
    print_section("5. CUSTOMER SUMMARIES")
    print(f"{'CUSTOMER':<12} {'RECORDS':>8} {'TOTAL QTY':>10} "
          f"{'TOTAL SPENDING':>17} {'DISTINCT PRODUCTS':>19}")
    print("-" * 72)
    for customer in sorted(customer_summary):
        data = customer_summary[customer]
        print(f"{customer:<12} {data['records']:>8} {data['quantity']:>10} "
              f"{data['spending']:>17.2f} {len(data['products']):>19}")

    # Assessment Data 6: Product Summaries
    print_section("6. PRODUCT SUMMARIES")
    print(f"{'PRODUCT':<14} {'RECORDS':>8} {'TOTAL QTY':>10} "
          f"{'TOTAL SALES':>15} {'CUSTOMERS':>12}")
    print("-" * 62)
    for product in sorted(product_summary):
        data = product_summary[product]
        print(f"{product:<14} {data['records']:>8} {data['quantity']:>10} "
              f"{data['sales']:>15.2f} {len(data['customers']):>12}")

    # Assessment Data 7: Ordered Results
    print_section("7. ORDERED RESULTS")
    print("Transactions sorted by transaction value (highest to lowest):")
    ordered_transactions = sorted(
        transactions,
        key=lambda record: (-record["transaction_value"], record["transaction_id"]),
    )
    for record in ordered_transactions:
        print(f"{record['transaction_id']} | {record['customer']} | "
              f"{record['product']} | Quantity: {record['quantity']} | "
              f"Value: {record['transaction_value']:.2f}")

    # Assessment Data 8: Overall Transaction Summary
    print_section("8. OVERALL TRANSACTION SUMMARY")
    print(f"Total transaction records: {len(transactions)}")
    print(f"Distinct customers: {len(distinct_customers)}")
    print(f"Distinct products: {len(distinct_products)}")
    print(f"Total quantity sold: {overall_quantity}")
    print(f"Overall transaction value: {overall_value:.2f}")
    print(f"Average transaction value: {overall_value / len(transactions):.2f}")
    print("Final Consolidated Transaction Report complete.")


if __name__ == "__main__":
    main()