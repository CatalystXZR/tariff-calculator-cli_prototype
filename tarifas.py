# -*- coding: utf-8 -*-
"""
CLI Prototype: "Tariff transport calculator for a private enterprise"

@Author: Matias Toledo (CatalystXZR)
@Created: 2025-08-25 23:34 
Version: 0.1-alpha (CLI prototype)

Description: 
Tariff transport calculator for a private enterprise
Designed with modular architecture for future integration with main systems.

License:
For internal use only. Redistribution or external deployment without explicit authorization from the author is strictly prohibited.

Dependencies: Python 3.10+, modules: datetime
"""

def tolls_function():
    """collect toll information and calculate total toll costs"""
    tolls = {}  # Dictionary with toll's info
    quantity_tolls = 0
    
    # Get number of tolls with validation
    while True:
        try:
            quantity_tolls = int(input("Toll's quantity: "))
            if quantity_tolls < 0:
                print("Please enter a non-negative number")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    
    # Collect toll information
    for i in range(quantity_tolls):
        name_toll = input(f"Enter the name of the #{i+1} toll: ").strip()
        while True:
            try:
                price = float(input(f"Enter the price of the {name_toll} toll: "))
                if price < 0:
                    print("Price cannot be negative. Please enter a valid amount.")
                    continue
                tolls[name_toll] = price
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
    
    total_tolls = round(sum(tolls.values()), 2)
    return tolls, total_tolls

def get_tariff_data():
    """Collect all necessary data for tariff calculation"""
    client = input('Client: ').strip()
    origin = input('Origin: ').strip()
    destination = input('Destination: ').strip()
    cargo_type = input('Type of Cargo: ').strip()
    
    # Get distance with validation
    while True:
        try:
            distance_km = float(input("Distance of trip (kms): "))
            if distance_km <= 0:
                print("Distance must be positive.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    
    # Get rate per km with validation
    while True:
        try:
            rate_per_km = float(input("Rate per km: "))
            if rate_per_km <= 0:
                print("Rate must be positive.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    
    # Get operational margin with validation
    while True:
        try:
            operational_margin = float(input("Operational margin (as decimal): "))
            if operational_margin < 0:
                print("Margin cannot be negative.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    
    # Get discounts with validation
    while True:
        try:
            discounts = float(input("Discounts (enter 0 if none): "))
            if discounts < 0:
                print("Discounts cannot be negative.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    
    return client, origin, destination, cargo_type, distance_km, rate_per_km, operational_margin, discounts

def calculate_tariff(tolls, total_tolls, client, origin, destination, cargo_type, 
                    distance_km, rate_per_km, operational_margin, discounts):
    """Calculate the final tariff based on all parameters"""
    # Calculate base transport cost
    base_cost = distance_km * rate_per_km
    
    # Add operational margin
    cost_with_margin = base_cost * (1 + operational_margin)
    
    # Add toll costs
    cost_with_tolls = cost_with_margin + total_tolls
    
    # Apply discounts
    final_cost = cost_with_tolls - discounts
    
    # Ensure cost doesn't be negative
    final_cost = max(0, final_cost)
    
    # Prepare results
    results = {
        'client': client,
        'origin': origin,
        'destination': destination,
        'cargo_type': cargo_type,
        'distance_km': distance_km,
        'rate_per_km': rate_per_km,
        'base_cost': round(base_cost, 2),
        'operational_margin_percent': operational_margin * 100,
        'cost_with_margin': round(cost_with_margin, 2),
        'tolls': tolls,
        'total_tolls': total_tolls,
        'cost_with_tolls': round(cost_with_tolls, 2),
        'discounts': discounts,
        'final_cost': round(final_cost, 2)
    }
    
    return results

def display_results(results):
    """display the results on a .txt archive"""
    with open('tarifas.txt', 'w') as f:
        f.write("="*10)
        f.write(" PROFORMA DE TRANSPORTE ")     
        f.write("="*10 + "\n")
        f.write(f"Client: {results['client']} \n")
        f.write(f"Route: {results['origin']} hacia {results['destination']}\n")
        f.write(f"Cargo Type: {results['cargo_type']}\n")
        f.write(f"Distance: {results['distance_km']} km \n")
        f.write(f"Rate per km: ${results['rate_per_km']:.2f}\n")
        f.write(f"Base transport cost: ${results['base_cost']:.2f}\n")
        f.write(f"Operational margin: {results['operational_margin_percent']:.1f}%\n")
        f.write(f"Cost with margin: ${results['cost_with_margin']:.2f}\n")
            
        f.write("\nTolls:\n")
        for toll, price in results['tolls'].items():
            f.write(f"  - {toll}: ${price:.2f}\n")
        f.write(f"Total tolls: ${results['total_tolls']:.2f}\n")
            
        f.write(f"\nCost with tolls: ${results['cost_with_tolls']:.2f}\n")
        f.write(f"Discounts applied: ${results['discounts']:.2f}\n")
        f.write("-"*10)
        f.write(f" FINAL TARIFF: ${results['final_cost']:.2f} ")
        f.write("-"*10)

def main():
    """main function to run the tariff calculator"""
        # Get all data
    tolls, total_tolls = tolls_function()
    client, origin, destination, cargo_type, distance_km, rate_per_km, operational_margin, discounts = get_tariff_data()
        
        # Calculate tariff
    results = calculate_tariff(
            tolls, total_tolls, client, origin, destination, cargo_type,
            distance_km, rate_per_km, operational_margin, discounts
        )
        
        # Display results
    display_results(results)
        
    return results

if __name__ == "__main__":
    main()
