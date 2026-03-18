from tools import get_revenue, get_stock_info


def research_company(ticker):

    revenue = get_revenue(ticker)

    info = get_stock_info(ticker)

    data = {"company_info": info, "revenue_data": revenue.to_string()}

    return data
