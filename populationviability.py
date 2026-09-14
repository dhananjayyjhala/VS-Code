# Import the random module so we can generate random lambda values each year.
import random


# This function simulates one population trajectory across a set number of years.
# It takes:
# - initial_population: starting number of individuals
# - carrying_capacity: maximum population the environment can support
# - lambda_min and lambda_max: range from which a random growth rate is selected each year
# - years: how many years to simulate (default is 100)
def simulate_population(initial_population, carrying_capacity, lambda_min, lambda_max, years=100):
    """
    Simulate a population over a fixed number of years.
    Each year, lambda is drawn uniformly at random from the supplied range.
    The population can never exceed carrying capacity and goes extinct at zero.
    """

    # Start with the initial population as a floating-point number so calculations can be fractional.
    population = float(initial_population)

    # Create variables to remember when the population hits the carrying capacity or goes extinct.
    # They stay as None until that event happens.
    carrying_capacity_year = None
    extinction_year = None

    # Loop once for each year in the simulation.
    # year starts at 1, so the first year is counted as year 1.
    for year in range(1, years + 1):
        # Randomly choose one yearly growth rate between the minimum and maximum lambda values.
        # Example: if lambda_min = 0.9 and lambda_max = 1.2, each year chooses a value in that range.
        lambda_value = random.uniform(lambda_min, lambda_max)

        # Update the population using the formula:
        # new population = current population * lambda
        population = population * lambda_value

        # If the population exceeds the carrying capacity, set it equal to the carrying capacity.
        # This keeps the population from growing above the maximum sustainable level.
        if population >= carrying_capacity:
            population = float(carrying_capacity)

            # Record the first year the population reaches carrying capacity.
            if carrying_capacity_year is None:
                carrying_capacity_year = year

        # If the population drops to zero or below, set it to zero and record extinction.
        # This happens once, the first time it becomes extinct.
        if population <= 0:
            population = 0.0
            if extinction_year is None:
                extinction_year = year

    # Return the final population, the year capacity was reached (if any), and the year extinction happened (if any).
    return population, carrying_capacity_year, extinction_year


# This function runs many different random simulations to create a bootstrap-style summary.
# A bootstrap approach repeats the same stochastic model many times to understand the range of likely outcomes.
def bootstrap_population_simulation(initial_population, carrying_capacity, lambda_min, lambda_max, runs=1000, years=100):
    """
    Run many random population trajectories to estimate the typical outcome.
    This is a bootstrap-style Monte Carlo simulation: each run draws a random lambda each year.
    """

    # These lists will store the final population from each simulation run.
    final_populations = []
    capacity_years = []
    extinction_years = []

    # Repeat the simulation many times.
    for _ in range(runs):
        # Run one simulation and get the final population and event years.
        final_population, carrying_capacity_year, extinction_year = simulate_population(
            initial_population,
            carrying_capacity,
            lambda_min,
            lambda_max,
            years,
        )

        # Save the final population for this run.
        final_populations.append(final_population)

        # If the population reached carrying capacity in this run, save the year it happened.
        if carrying_capacity_year is not None:
            capacity_years.append(carrying_capacity_year)

        # If the population went extinct in this run, save the year it happened.
        if extinction_year is not None:
            extinction_years.append(extinction_year)

    # Calculate summary statistics across all runs.
    return {
        # Average final population across all runs.
        "average_final_population": sum(final_populations) / runs,

        # Lowest and highest final population seen in the simulations.
        "final_population_range": (min(final_populations), max(final_populations)),

        # Average year that carrying capacity was reached, but only if it ever happened.
        "average_capacity_year": sum(capacity_years) / len(capacity_years) if capacity_years else None,

        # Average year extinction happened, but only if it ever happened.
        "average_extinction_year": sum(extinction_years) / len(extinction_years) if extinction_years else None,

        # Probability of hitting carrying capacity in a random run.
        "probability_of_reaching_capacity": len(capacity_years) / runs,

        # Probability of extinction in a random run.
        "probability_of_extinction": len(extinction_years) / runs,
    }


# This block only runs when the file is executed directly, not when it is imported elsewhere.
if __name__ == "__main__":
    try:
        # Ask the user for the starting conditions.
        # These values define the population model.
        initial_population = float(input("Enter the current population size: "))
        carrying_capacity = float(input("Enter the carrying capacity: "))
        lambda_min = float(input("Enter the minimum lambda value for the range: "))
        lambda_max = float(input("Enter the maximum lambda value for the range: "))

        # Check that the inputs are realistic.
        # Lambda must be greater than 0 because it is a multiplication factor.
        if lambda_min <= 0 or lambda_max <= 0:
            raise ValueError("Lambda values must be greater than zero.")

        # Carrying capacity must also be positive.
        if carrying_capacity <= 0:
            raise ValueError("Carrying capacity must be greater than zero.")

        # Population cannot be negative.
        if initial_population < 0:
            raise ValueError("Population cannot be negative.")

        # Run one simulation for 100 years and store the key results.
        final_population, capacity_year, extinction_year = simulate_population(
            initial_population,
            carrying_capacity,
            lambda_min,
            lambda_max,
            years=100,
        )

        # Print the main results for this one simulation.
        print("\nPopulation viability simulation")
        print(f"Initial population: {initial_population}")
        print(f"Carrying capacity: {carrying_capacity}")
        print(f"Lambda range: {lambda_min} to {lambda_max}")
        print(f"Population after 100 years: {final_population:.2f}")

        # If the population reached carrying capacity, print the year it happened.
        if capacity_year is not None:
            print(f"The population reached carrying capacity in year {capacity_year}.")
        else:
            print("The population did not reach carrying capacity within 100 years.")

        # If the population went extinct, print the year it happened.
        if extinction_year is not None:
            print(f"The population went extinct in year {extinction_year}.")
        else:
            print("The population did not go extinct within 100 years.")

        # Run a bootstrap summary with 1000 random trajectories to estimate patterns over many possible outcomes.
        summary = bootstrap_population_simulation(
            initial_population,
            carrying_capacity,
            lambda_min,
            lambda_max,
            runs=1000,
            years=100,
        )

        # Print the bootstrap summary results.
        print("\nBootstrap summary over 1000 random trajectories")
        print(f"Average final population: {summary['average_final_population']:.2f}")
        print(f"Probability of reaching carrying capacity: {summary['probability_of_reaching_capacity'] * 100:.1f}%")
        print(f"Probability of extinction: {summary['probability_of_extinction'] * 100:.1f}%")

    # If the user enters invalid and impossible values, show a clear error message.
    except ValueError as e:
        print(f"Input error: {e}")
        print("Please enter valid positive numbers.")
