#Robinhood API
import robin_stocks.robinhood as rh
from datetime import datetime


# Step 1: Login to Robinhood
USERNAME ="JohnDoe@hotmail.com"
PASSWORD ="Abc123"

rh.login(USERNAME, PASSWORD)

# Get the nearest expiration date for SPY options
def get_nearest_expiration(symbol="SPY"):
    dates = r.options.get_chains(symbol)['expiration_dates']
    return dates[0] if dates else None

# Fetch SPY put options for the nearest expiration date
def fetch_put_options(symbol="SPY"):
    expiration = get_nearest_expiration(symbol)
    if not expiration:
        print("🚨 No expiration dates found for SPY.")
        return []

    options = r.options.find_options_by_expiration(symbol, expiration)
    return [opt for opt in options if opt["type"] == "put"]

# Display all buy (bid) and sell (ask) prices next to each other and sort by strike price
def display_buy_sell_puts():
    put_options = fetch_put_options()
    if not put_options:
        return

    # Sort options by strike price in ascending order (lower strike price = higher premium)
    put_options.sort(key=lambda opt: float(opt["strike_price"]))

    print(f"\n📅 SPY Put Options ({get_nearest_expiration()}):\n")
    print(f"{'Strike':<8} {'Buy (Bid)':<10} {'Sell (Ask)':<10}")
    print("-" * 30)

    for opt in put_options:
        strike = opt["strike_price"]
        bid = opt.get("bid_price", "N/A")
        ask = opt.get("ask_price", "N/A")

        # Correctly label the bid and ask prices
        print(f"{strike:<8} {ask:<10} {bid:<10}")

    return put_options

# Implement a three-way butterfly option strategy
def three_way_butterfly(symbol="SPY"):
    put_options = fetch_put_options(symbol)
    if not put_options:
        return

    # Find the closest strike prices for the three-way butterfly
    strike_prices = sorted(set([float(opt["strike_price"]) for opt in put_options]))  # Convert to float
    if len(strike_prices) < 3:
        print("🚨 Not enough strike prices for a three-way butterfly strategy.")
        return

    # Select middle strike for selling two options
    middle_strike = round(strike_prices[len(strike_prices) // 2])  # Round to nearest integer
    higher_strike = middle_strike + 1  # Adjust according to market conditions
    lower_strike = middle_strike -1 # Adjust according to market conditions
#ignore
    print(f"\n📅 Three-Way Butterfly Strategy for {symbol} Options (Expiration: {get_nearest_expiration()}):")
    print(f"Buy {lower_strike} Put, Sell 2 x {middle_strike} Puts, Buy {higher_strike} Put")

    # Display options for selected strikes
    lower_strike_option = next((opt for opt in put_options if float(opt["strike_price"]) == lower_strike), None)
    middle_strike_option = next((opt for opt in put_options if float(opt["strike_price"]) == middle_strike), None)
    higher_strike_option = next((opt for opt in put_options if float(opt["strike_price"]) == higher_strike), None)

#Quality Control
    if lower_strike_option and middle_strike_option and higher_strike_option:
        print(f"Lower Strike ({lower_strike}): {lower_strike_option['ask_price']}")
        print(f"Middle Strike ({middle_strike}): {middle_strike_option['ask_price']}")
        print(f"Higher Strike ({higher_strike}): {higher_strike_option['ask_price']}")
    else:
        print("🚨 Could not find all the required strike options.")

# Run the function to display three-way butterfly
three_way_butterfly()



#MFA DOES NOT WORK. Robinhood Security Update.
