**Basic PVA**

This program provides a simple baseline for exploring population change over 100 years. Its inputs are the initial population 
size, carrying capacity, and annual population growth multiplier (lambda). Initial population represents the number of 
individuals at the beginning, while carrying capacity sets the maximum population permitted by the model. Lambda determines
annual change: values below 1 produce decline, values above 1 produce growth, and a value of 1 maintains the population.

With a fixed lambda, each year’s population is calculated by multiplying the previous population by the same growth 
multiplier and capping the result at carrying capacity. This produces a predictable trajectory that illustrates how sustained
growth or decline affects population size. It serves as a baseline for comparison with a model that incorporates annual 
variation.

**PVA with Stochasticity**

This program explores population change under variable annual growth, differences in environmental carrying capacity,
and occasional disasters. It extends a simple population projection by allowing multiple possible outcomes under
the same starting conditions.

Population growth and lambda

The initial population sets the starting number of individuals. Each year, population is multiplied by a randomly 
selected growth multiplier, lambda. Values below 1 cause decline, values above 1 cause growth, and a value of 1
produces no change before other effects are applied.

Lambda is sampled from a truncated normal distribution, defined by a user-specified central value and minimum and
maximum bounds. This makes growth multipliers near the distribution’s centre more likely than values farther away.
Values outside the specified bounds are rejected and sampled again.

The standard deviation is set to one-quarter of the difference between the maximum and minimum lambda. A wider 
range therefore allows greater annual variation, while a narrower range produces more consistent growth. These 
bounds should represent biologically plausible annual growth conditions. The supplied mean is the centre of the 
underlying normal distribution; truncation can shift the actual average of the sampled values, particularly when 
the centre is near a boundary.

Variation in carrying capacity

Carrying capacity represents the population limit supported by the environment. At the beginning of each 
simulation run, an effective carrying capacity is selected uniformly between 95% and 105% of the supplied value.
It remains fixed during that run. This represents differences or uncertainty in environmental capacity across possible 
scenarios.

Disaster events

The disaster-probability input specifies the chance of a disaster in each year. For example, 0.05 represents a 
5% annual chance. Events are checked independently each year, so multiple disasters can occur within one trajectory.

In the current implementation, a disaster first reduces population to 25% of its pre-disaster size, then multiplies
the remainder by a randomly selected value between 0.40 and 0.60. Together, these reductions leave 10–15% of the
pre-disaster population. The program records the first disaster year.

**Why include stochasticity?**

Random annual growth and occasional population crashes represent sources of variability that a constant-growth projection
cannot capture. Different sequences of favourable years, poor years, and disasters can produce different population
outcomes even when the starting conditions are identical. Repeating the simulation allows these possible outcomes to
be compared.

This remains a simplified educational model. Its usefulness depends on whether the growth bounds, carrying-capacity 
variation, and disaster assumptions reflect the population being studied. These random components represent environmental
variation; they do not explicitly model individual births and deaths.
