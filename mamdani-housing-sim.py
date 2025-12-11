import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------Configuration-------------------------------
CONFIG = {
    # Sim settings
    "n_sims": 10000,
    "horizon_years": 10,

    # Budget baselines
    "total_city_budget_annual": 112400000000,
    "baseline_housing_budget_annual": 1600000000,

    # Cap choice
    # "housing_share" is extra spending cap is a % of baseline housing budget over 10 years
    "cap_type": "housing_share",

    "cap_pct": 1.0,
}

#-----------------------------Policy Assumptions-----------------------------
POLICIES = {
    "rent_freeze_tenant_supports": {
        "mean_annual": 900000000,
        "std_annual": 300000000,
    },

    "affordable_units_200k": {
        "mean_annual": 8000000000,
        "std_annual": 2000000000,
    },

    "tenant_protection": {
        "mean_annual": 400000000,
        "std_annual": 150000000,
    },
    
    "homeowner_tax": {
        "mean_annual": -800000000,
        "std_annual": 400000000,
    },
}

#-------------------------------helper functions-------------------------------

def compute_cap(config:dict) -> float:
    years = config["horizon_years"]
    housing_base_10yr = config["baseline_housing_budget_annual"] * years
    total_budget_10yr = config["total_city_budget_annual"] * years
    cap_pct = config["cap_pct"]

    if config["cap_type"] == "housing_share":
        cap = housing_base_10yr * cap_pct
    else:
        raise ValueError(f"Unknown cap_type: {config['cap_type']}")
    
    return cap

def simulate_one_path(config: dict, policies: dict) -> float:
    years = config["horizon_years"]
    total_cost_10yr = 0.0

    for year in range(years):
        annual_total = 0.0
        for policy_name, params in policies.items():
            mean = params["mean_annual"]
            std = params["std_annual"]
            draw = np.random.normal(loc=mean, scale=std)
            annual_total += draw
        total_cost_10yr += annual_total
    return total_cost_10yr

def run_simulation(config: dict, policies: dict) -> pd.DataFrame:
    n_sims = config["n_sims"]
    cap = compute_cap(config)

    total_costs = np.zeros(n_sims, dtype=float)
    breaches = np.zeros(n_sims, dtype=bool)

    for i in range(n_sims):
        total_cost_10yr = simulate_one_path(config, policies)
        total_costs[i] = total_cost_10yr
        breaches[i] = total_cost_10yr > cap

    df = pd.DataFrame({
        "total_incremental_cost_10yr": total_costs,
        "breach_cap": breaches,
    }) 
    return df, cap

def summarize_results(df: pd.DataFrame, cap: float, config:dict) -> None:
    total_costs = df["total_incremental_cost_10yr"]

    mean_cost = total_costs.mean()
    median_cost = total_costs.median()
    p5 = total_costs.quantile(0.05)
    p95 = total_costs.quantile(0.95)
    breach_prob = df["breach_cap"].mean()

    years = config["horizon_years"]
    cap_pct = config["cap_pct"]
    cap_type = config["cap_type"]

    print("--------------------------Config--------------------------")
    print(f"Number of Sims:                 {config['n_sims']}")
    print(f"Horizon (years):                {years}")
    print(f"Cap type:                       {cap_type}")
    print(f"Cap Percent:                    {cap_pct:.2%}")
    print("----------------------------------------------------------")
    print(f"Ten year cap (dollars):         ${cap:,.0f}")
    print()
    print("---------------------Cost Distribution---------------------")
    print(f"Mean 10yr cost:                 ${mean_cost:,.0f}")
    print(f"Median 10yr cost:               ${median_cost:,.0f}")
    print(f"5th percentile (cheap):         ${p5:,.0f}")
    print(f"95th percentile (expensive):    ${p95:,.0f}")
    print()
    print("------------------------Fiscal Risk------------------------")
    print(f"Probability of reaching Breach cap:    {breach_prob:.1%}")
    print(f"Probability of staying within cap:     {(1 - breach_prob):.1%}")

def plot_results(df: pd.DataFrame, cap: float) -> None:
    total_costs = df["total_incremental_cost_10yr"]

    plt.figure()
    plt.hist(total_costs / 1000000000, bins=50)
    plt.axvline(cap / 1000000000, linestyle="--")

    plt.xlabel("Total 10-year incremental cost (billions of $)")
    plt.ylabel("Frequency across simulations")
    plt.title("Distribution of 10-Year Incremental Cost for Housing Agenda")

    ymax = plt.ylim()[1]
    plt.text(cap / 1000000000, 0.9 * ymax, "Cap", rotation = 90, va = "top", ha= "right")

    plt.tight_layout()
    plt.show()

#---------------------------------Main-----------------------------------
def main():
    df, cap = run_simulation(CONFIG, POLICIES)
    summarize_results(df,cap,CONFIG)
    plot_results(df,cap)
    print("Simulation Finished")

if __name__ == "__main__":
    main()
