# N-Body-Simulator
Simulation of multiple non-zero mass particles interacting with each other via their gravitational fields using the 4th order Runge-Kutta method to solve a 2nd order ODE (Ordinary Differential Equation).

## How it works
### Intro
The force of gravity between two masses is as described from Newton's Law of Universal Gravitation $$F = \frac{G M_1 M_2}{{r}^2}$$ where $r$ is the distance of the two bodies from the center.
However, in the equation above, force is described as a scalar, whereas force should be described as a vector. Thus, the unit vector of $r$ is needed.
$$\vec F = \frac{G M_1 M_2}{r^2}\hat r$$ where $\hat r = \frac{\vec r}{||\vec r||}$.
Giving us the final equation $$\vec F = \frac{G M_1 M_2 \vec r}{r^3}$$
When simulating velocity, and as a result - position, force is not all that usefull compared to acceleration. However Newton's second Law $\vec F=m\vec a$ means finding acceleration is very easy. If we want to find the acceleration of $M_2$, we sub in Newton's second law.
$$\cancel{M_2} \vec a = \frac{G M_1 \cancel{M_2} \vec r}{r^3}$$
The masses will cancel out because the mass of the object that's being accelerated does not matter. Acceleration in a gravitational field at a certain point will always remain constant. Let's also note that since $G$ is a constant, and the mass of a body will remain constant, we can reduce $GM$ to a single variable $\mu$ which is called the standard gravitational parameter.
So the final equation is $$\vec a = \frac{\mu \vec r}{r^3} \tag 1$$ where $\mu$ is the standard gravitational parameter of the mass creating the gravitational field.
<br/>
<br/>
It is important to note that in equation $(1)$, the mass creating the gravitational field is centered at the origin of the coordinate system. Hence why the use of just multiplying the vector is sufficient. Moreover, equation $(1)$ only works if there are 2 bodies. As soon as there is a third body, a given mass will be affected by the force of gravity of two other masses. This can be solved by summing up all the forces or accelerations of all the other bodies. For example, supposed we have three masses $M_1, M_2, M_3$. The acceleration of $M_2$ is $$\vec{a_2} = \frac{\mu_1 (\vec{r_1}-\vec{r_2})}{||\vec{r_1}-\vec{r_2}||^3}+\frac{\mu_3 (\vec{r_3}-\vec{r_2})}{||\vec{r_3}-\vec{r_2}||^3}$$ Here, no mass is the center (origin) of the frame of reference. Thus subtracting the vector is necessary to obtain the distance between two masses. Similarly, if we have 5 masses, we can find the acceleration of $M_3$ with
$$\vec{a_3} = \frac{\mu_1 (\vec{r_1}-\vec{r_3})}{||\vec{r_1}-\vec{r_3}||^3}+\frac{\mu_2 (\vec{r_2}-\vec{r_3})}{||\vec{r_2}-\vec{r_3}||^3}+\frac{\mu_4 (\vec{r_4}-\vec{r_3})}{||\vec{r_4}-\vec{r_3}||^3}+\frac{\mu_5 (\vec{r_5}-\vec{r_3})}{||\vec{r_5}-\vec{r_3}||^3}$$
<br/>
<br/>
We can generalize this equation so that it can work for any number of masses. If we have a set of $n$ masses $\\{M_1, M_2, \dots, M_{n-1}, M_n\\}$, then the acceleration of the x-th mass in the set can be found with $$\vec{a_x} = \sum_{\substack{i=1 \\\ i\neq x}}^n \frac{\mu_i(\vec{r_i}-\vec{r_x})}{{||\vec{r_i}-\vec{r_x}||}^3} \quad \\{x, n \in \mathbb{N} \mid x \leq n\\} \tag 2$$
<br/>
### The Computer Program
<br/>
To compute the position, velocity and acceleration of all masses, we need to compute equation $(2)$ for each mass in the set (e.g. $\vec{a_1}, \dots, \vec{a_n}$). An orbital state vector is a pair of vectors. $(\vec{r}, \vec{v})$ is a state vector which can ultimately be broken down into $[r_x, r_y, v_x, v_y]$. State vectors describe the trajectory of a mass in any point in time. If two masses start with the same state vectors, they will have the exact same trajectories. 
<br/>
Thus we start each mass with an initial state vector, and a pre-determined time step. Since there is no general analytical solution to the N-body problem, we must approximate the solution using numerical methods. What we are doing is using the RK-4 method to solve a 2nd order ODE with a given time step. Carrying on, we then compute the acceleration of each mass using equation $(2)$. The derivative of the current step is the velocity of the current step and the acceleration of the current step. So the derivative of the state vector becomes $[v_x, v_y, a_x, a_y]$. Using the RK-4 method, the next state vector is found with new position and velocity vectors. And acceleration is computed again, and this process repeats many times to propagate the mass through time.
