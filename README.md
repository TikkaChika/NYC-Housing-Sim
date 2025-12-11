# NYC-Housing-Sim
NYC Housing Investment Monte Carlo Model

This project simulates the 10-year fiscal impact of a large housing agenda proposed for New York City. The model estimates annual costs for major policy areas, including affordable housing construction, NYCHA capital work, rent supports, and tenant protection programs. It also includes expected savings from homeowner tax reforms.

A Monte Carlo model estimating the 10-year cost of NYC’s proposed $100B housing plan. Simulates policy costs, tax savings, and budget uncertainty, then tests whether the plan fits within an expanded housing-budget cap. This does not account for revenue generated during the 10 years.

Features

Models key policy cost areas with adjustable assumptions

Uses a Monte Carlo simulation to show a full range of outcomes

Applies a cap based on a multiple of the current housing budget

Produces summary statistics and a cost distribution plot

How to Run

Clone the repo

Create and activate a virtual environment

Install dependencies:

pip install numpy pandas matplotlib


Run the model:

python mamdani-housing-sim.py

File Structure
mamdani-housing-sim.py       # model, simulation, plots
README.md                    # project overview

Purpose

The goal is to estimate whether a large housing investment plan can fit within a scaled-up housing budget over a 10-year period. The simulation is not a forecast. It gives a simple way to explore fiscal risk and budget uncertainty.

Limitations

This model focuses on incremental costs and direct savings. It does not account for new revenue the plan may generate, such as long-term tax gains, economic growth, or outside funding. Those would need a separate revenue model.
