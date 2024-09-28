import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def get_monthly_returns(ticker: str, start_date: str, end_date: str = None) -> list:
    """
    Fetch historical monthly percentage returns for the given stock ticker.

    Args:
    ticker: str: The stock ticker symbol (e.g., 'SPY' for S&P 500)
    start_date: str: The start date in "mm/yyyy" format
    end_date: str: The end date in "mm/yyyy" format (optional, defaults to today)

    Returns:
    list: A list of monthly returns as percentages.
    """
    # Convert the start date to datetime object
    start_date_dt = datetime.strptime(start_date, "%m/%Y")

    # Use today's date if no end date is provided
    if end_date is None:
        end_date_dt = datetime.today()
    else:
        end_date_dt = datetime.strptime(end_date, "%m/%Y")

    # Download historical data from Yahoo Finance
    stock_data = yf.download(
        ticker, start=start_date_dt, end=end_date_dt, interval="1mo"
    )

    # Calculate monthly returns as percentage change
    stock_data["Monthly Return"] = stock_data["Adj Close"].pct_change() * 100

    # Drop the first NaN return and convert to list
    monthly_returns = stock_data["Monthly Return"].dropna().tolist()

    return monthly_returns


def profit(
    initial_investment: float = 0.0,
    monthly_investment: float = 0.0,
    monthly_returns: list = None,
    start_date: str = "01/2020",
    end_date: str = None,
    ticker: str = "SPY",
) -> None:
    """
    Function to calculate the profit of the stock market based on historical monthly returns.

    Args:
    initial_investment: float: Initial investment amount
    monthly_investment: float: Monthly investment amount
    monthly_returns: list: List of monthly returns as percentages (optional, fetched from API if None)
    start_date: str: Start date in the format "mm/yyyy"
    end_date: str: End date in the format "mm/yyyy" (optional, defaults to today)
    ticker: str: Stock ticker to fetch monthly returns (default is 'SPY' for S&P 500)

    Returns:
    void
    """
    if monthly_returns is None:
        monthly_returns = get_monthly_returns(ticker, start_date, end_date)

    total_investment = initial_investment
    total_value = total_investment

    print(
        f"{'Month':<10}{'Total Investment':<20}{'Total Value':<20}{'Total Profit':<20}{'Monthly Profit':<20}"
    )
    print("=" * 90)

    start_date_dt = datetime.strptime(start_date, "%m/%Y")

    for month in range(1, len(monthly_returns) + 1):
        # Add monthly investment before calculating returns
        total_investment += monthly_investment
        total_value += monthly_investment

        # Calculate monthly profit from the current total value
        monthly_profit = total_value * (monthly_returns[month - 1] / 100)
        total_value += monthly_profit

        total_profit = total_value - total_investment

        # Format the date for the current month
        current_month = (start_date_dt + timedelta(days=(month - 1) * 30)).strftime(
            "%m/%Y"
        )

        print(
            f"{current_month:<10}{total_investment:<20.2f}{total_value:<20.2f}{total_profit:<20.2f}{monthly_profit:<20.2f}"
        )


def profit_as_graph(
    initial_investment: float = 0.0,
    monthly_investment: float = 0.0,
    monthly_returns: list = None,
    start_date: str = "01/2020",
    end_date: str = None,
    ticker: str = "SPY",
) -> None:
    """
    Function to calculate the profit of the stock market based on historical monthly returns and plot as a graph.

    Args:
    initial_investment: float: Initial investment amount
    monthly_investment: float: Monthly investment amount
    monthly_returns: list: List of monthly returns as percentages (optional, fetched from API if None)
    start_date: str: Start date in the format "mm/yyyy"
    end_date: str: End date in the format "mm/yyyy" (optional, defaults to today)
    ticker: str: Stock ticker to fetch monthly returns (default is 'SPY' for S&P 500)

    Returns:
    void
    """

    if monthly_returns is None:
        monthly_returns = get_monthly_returns(ticker, start_date, end_date)

    total_investment = initial_investment
    total_value = total_investment

    x = []
    total_value_list = []
    total_investment_list = []
    total_profit_list = []
    monthly_profit_list = []

    start_date_dt = datetime.strptime(start_date, "%m/%Y")

    for month in range(1, len(monthly_returns) + 1):
        # Add monthly investment before calculating returns
        total_investment += monthly_investment
        total_value += monthly_investment

        # Calculate monthly profit from the current total value
        monthly_profit = total_value * (monthly_returns[month - 1] / 100)
        total_value += monthly_profit

        total_profit = total_value - total_investment

        # Format the date for the current month
        current_month = (start_date_dt + timedelta(days=(month - 1) * 30)).strftime(
            "%m/%Y"
        )

        x.append(current_month)
        total_value_list.append(total_value)
        total_investment_list.append(total_investment)
        total_profit_list.append(total_profit)
        monthly_profit_list.append(monthly_profit)

    # Plotting the data
    plt.figure(figsize=(12, 6))

    # Plot total value over time
    plt.plot(x, total_value_list, marker="o", color="blue", label="Total Value ($)")

    # Plot total investment over time
    plt.plot(
        x,
        total_investment_list,
        marker="o",
        color="green",
        label="Total Investment ($)",
    )

    # Plot total profit over time
    plt.plot(x, total_profit_list, marker="o", color="red", label="Total Profit ($)")

    # Plot monthly profit
    plt.bar(
        x, monthly_profit_list, color="orange", alpha=0.5, label="Monthly Profit ($)"
    )

    # Adding title and labels
    plt.title(f"Investment, Value, and Profit Over Time ({ticker})", fontsize=16)
    plt.xlabel("Month/Year", fontsize=12)
    plt.ylabel("Amount ($)", fontsize=12)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Show grid
    plt.grid(True)

    # Adding a legend
    plt.legend(loc="upper left")

    # Adjust layout for readability
    plt.tight_layout()

    # Show the plot
    plt.show()


if __name__ == "__main__":
    # Example usage with real historical data
    # profit(
    #     initial_investment=30000,
    #     monthly_investment=1500,
    #     start_date="01/2000",  # Starting from January 2000
    #     end_date=None,  # Default to today's date if not provided
    #     ticker="SPY",  # S&P 500 ETF
    # )

    profit_as_graph(
        initial_investment=30000,
        monthly_investment=1500,
        start_date="01/1984",  # Starting from January 2000
        end_date=None,  # Default to today's date if not provided
        ticker="SPY",  # S&P 500 ETF
    )
