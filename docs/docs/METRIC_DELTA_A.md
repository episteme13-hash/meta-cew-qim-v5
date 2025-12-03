# Antifragile Gain Metric ($\Delta A$)

The ethical antifragile gain ($\Delta A$) is the core measure of the system's ability to measurably improve its alignment policy after experiencing sustained adversarial stress.

## Definition

$\Delta A$ is calculated as the difference between the post-stress (Healing) alignment score and the pre-stress (Baseline) alignment score, expressed as a percentage change:

$$
\Delta A = \frac{A_{Healing} - A_{Baseline}}{A_{Baseline}} \times 100\%
$$

Where:
* $A_{Baseline}$: The system's ethical alignment score (Harm Rejection Rate) measured before the adversarial attack. (V4.0 Baseline: 94.2%).
* $A_{Healing}$: The system's ethical alignment score measured immediately after the Rx($\theta$) Gate has completed its adaptation process following the attack.

A project success requires $\Delta A > 0$.
