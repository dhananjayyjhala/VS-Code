# This script models a population over time using a random growth rate each year.
# It includes:
# - a mean lambda value and a distribution around it
# - a range for lambda (minimum and maximum)
# - a yearly probability of disaster causing a population crash
# - a carrying capacity that can vary by +/- 5% each run
# - a bootstrap simulation with 1000 repeated runs and a final graph

import random

# Try to import matplotlib for the final graph.
# If it is not installed, the script will still run without plotting.
try:
    import matplotlib
    matplotlib.use("Agg")  # Use a non-interactive backend so the script runs in headless environments.
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


# This function samples a lambda value from a normal distribution centered on the mean.
# The distribution is constrained to stay within the user-provided min and max range.
# This means the growth rate is most likely close to the average lambda, but can vary around it.
def sample_lambda(lambda_mean, lambda_min, lambda_max):
    # Make sure the user mean is inside the valid range.
    # If the user gives a value outside the range, clamp it to the nearest boundary.
    lambda_mean = min(max(lambda_mean, lambda_min), lambda_max)

    # The spread of the normal distribution is based on the width of the lambda range.
    # Using a quarter of the range gives a reasonable spread: most values stay inside the min-max interval.
    sigma = (lambda_max - lambda_min) / 4.0

    # If the range is extremely narrow, the spread is effectively zero.
    if sigma <= 0:
        return lambda_mean

    # Draw a random value from a normal distribution centered on the mean.
    lambda_value = random.gauss(lambda_mean, sigma)

    # Keep resampling until the value falls inside the allowed range.
    while lambda_value < lambda_min or lambda_value > lambda_max:
        lambda_value = random.gauss(lambda_mean, sigma)

    return lambda_value


# This function simulates one population trajectory over a set number of years.
# It uses a random lambda each year, a possible disaster crash, and a carrying capacity that may vary by +/- 5%.
def simulate_population(initial_population, carrying_capacity, lambda_mean, lambda_min, lambda_max, disaster_probability=0.0, years=100):
    """
    Simulate one population run for a fixed number of years.
    Each year, lambda is chosen from a normal distribution centered on the mean lambda.
    The population may also crash due to a stochastic disaster event.
    """

    # Convert to float so calculations can be fractional.
    population = float(initial_population)

    # Each run can have a slightly different carrying capacity within +/- 5% of the user input.
    # This reflects environmental variability from year to year.
    effective_capacity = carrying_capacity * random.uniform(0.95, 1.05)

    # Track the year when the population first hits its capacity or goes extinct.
    carrying_capacity_year = None
    extinction_year = None
    disaster_year = None

    # Loop from year 1 to the requested number of years.
    for year in range(1, years + 1):
        # Sample a growth rate for this year around the mean lambda.
        lambda_value = sample_lambda(lambda_mean, lambda_min, lambda_max)

        # Update the population according to the yearly growth rate.
        population = population * lambda_value

        # Disaster event: a random yearly chance of a major population crash.
        # If a random value is less than the disaster probability, a crash happens.
        if random.random() < disaster_probability:
            # A disaster cuts the population sharply.
            # Here, a crash reduces the population to 25% of its current level.
            population = population * 0.25

            # Record the first crash year.
            if disaster_year is None:
                disaster_year = year

        # If the population exceeds the carrying capacity, cap it there.
        if population >= effective_capacity:
            population = float(effective_capacity)
            if carrying_capacity_year is None:
                carrying_capacity_year = year

        # If the population drops to or below zero, set it to zero and record extinction.
        if population <= 0:
            population = 0.0
            if extinction_year is None:
                extinction_year = year

    # Return the final population and the year of each key event.
    return population, carrying_capacity_year, extinction_year, disaster_year


# This function runs 1000 random bootstrap simulations to estimate the likely population outcomes.
def bootstrap_population_simulation(initial_population, carrying_capacity, lambda_mean, lambda_min, lambda_max, disaster_probability=0.0, runs=1000, years=100):
    """
    Run many stochastic simulations and summarize their outcomes.
    This creates the bootstrap distribution of final population sizes.
    """

    # Store the final population from each run.
    final_populations = []
    capacity_years = []
    extinction_years = []
    disaster_years = []

    # Repeat the simulation many times.
    for _ in range(runs):
        final_population, carrying_capacity_year, extinction_year, disaster_year = simulate_population(
            initial_population,
            carrying_capacity,
            lambda_mean,
            lambda_min,
            lambda_max,
            disaster_probability,
            years,
        )

        final_populations.append(final_population)

        if carrying_capacity_year is not None:
            capacity_years.append(carrying_capacity_year)

        if extinction_year is not None:
            extinction_years.append(extinction_year)

        if disaster_year is not None:
            disaster_years.append(disaster_year)

    # Calculate summary statistics.
    summary = {
        "average_final_population": sum(final_populations) / runs,
        "final_population_range": (min(final_populations), max(final_populations)),
        "average_capacity_year": sum(capacity_years) / len(capacity_years) if capacity_years else None,
        "average_extinction_year": sum(extinction_years) / len(extinction_years) if extinction_years else None,
        "average_disaster_year": sum(disaster_years) / len(disaster_years) if disaster_years else None,
        "probability_of_reaching_capacity": len(capacity_years) / runs,
        "probability_of_extinction": len(extinction_years) / runs,
        "probability_of_disaster": len(disaster_years) / runs,
        "final_populations": final_populations,
    }

    # Make the final bootstrap graph if matplotlib is available.
    if plt is not None:
        plt.figure(figsize=(10, 6))
        plt.hist(final_populations, bins=25, color="steelblue", edgecolor="black")
        plt.title("Distribution of Final Population Sizes Across 1000 Bootstrap Runs")
        plt.xlabel("Final population after 100 years")
        plt.ylabel("Number of runs")
        plt.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        plt.show()

    return summary


# This block runs only when the script is executed directly.
if __name__ == "__main__":
    try:
        # Ask the user for the population and model parameters.
        initial_population = float(input("Enter the current population size: "))
        carrying_capacity = float(input("Enter the carrying capacity: "))
        lambda_min = float(input("Enter the minimum lambda value: "))
        lambda_mean = float(input("Enter the average lambda value: "))
        lambda_max = float(input("Enter the maximum lambda value: "))
        disaster_probability = float(input("Enter the probability of a population crash each year (between 0 and 1): "))

        # Check that the inputs are valid.
        if lambda_min <= 0 or lambda_mean <= 0 or lambda_max <= 0:
            raise ValueError("All lambda values must be greater than zero.")
        if lambda_min > lambda_mean or lambda_mean > lambda_max:
            raise ValueError("The mean lambda must lie between the minimum and maximum lambda values.")
        if carrying_capacity <= 0:
            raise ValueError("Carrying capacity must be greater than zero.")
        if initial_population < 0:
            raise ValueError("Population cannot be negative.")
        if not (0 <= disaster_probability <= 1):
            raise ValueError("Disaster probability must be between 0 and 1.")

        # Run one representative simulation for 100 years.
        final_population, capacity_year, extinction_year, disaster_year = simulate_population(
            initial_population,
            carrying_capacity,
            lambda_mean,
            lambda_min,
            lambda_max,
            disaster_probability,
            years=100,
        )

        # Print the main results for that single simulation.
        print("\nPopulation viability simulation")
        print(f"Initial population: {initial_population}")
        print(f"Carrying capacity: {carrying_capacity}")
        print(f"Lambda range: {lambda_min} to {lambda_max}")
        print(f"Mean lambda: {lambda_mean}")
        print(f"Yearly disaster probability: {disaster_probability:.3f}")
        print(f"Population after 100 years: {final_population:.2f}")

        if capacity_year is not None:
            print(f"The population reached carrying capacity in year {capacity_year}.")
        else:
            print("The population did not reach carrying capacity within 100 years.")

        if extinction_year is not None:
            print(f"The population went extinct in year {extinction_year}.")
        else:
            print("The population did not go extinct within 100 years.")

        if disaster_year is not None:
            print(f"A population crash occurred in year {disaster_year}.")
        else:
            print("No major population crash occurred in this simulation.")

        # Run the full 1000-run bootstrap simulation and show the plot.
        summary = bootstrap_population_simulation(
            initial_population,
            carrying_capacity,
            lambda_mean,
            lambda_min,
            lambda_max,
            disaster_probability,
            runs=1000,
            years=100,
        )

        print("\nBootstrap summary over 1000 random trajectories")
        print(f"Average final population: {summary['average_final_population']:.2f}")
        print(f"Probability of reaching carrying capacity: {summary['probability_of_reaching_capacity'] * 100:.1f}%")
        print(f"Probability of extinction: {summary['probability_of_extinction'] * 100:.1f}%")
        print(f"Probability of a population crash: {summary['probability_of_disaster'] * 100:.1f}%")

    # Catch invalid inputs and display a clear message.
    except ValueError as e:
        print(f"Input error: {e}")
        print("Please enter valid values for the population, carrying capacity, lambda range, and disaster probability.")
