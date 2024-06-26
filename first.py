# Import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import shiny

# Define the UI
app_ui = shiny.ui.page_fluid(
    shiny.ui.layout_sidebar(
        shiny.ui.panel_sidebar(
            shiny.ui.input_slider(
                "steps", "Number of steps:", min=100, max=10000, value=1000
            ),
            shiny.ui.input_action_button(
                "simulate", "Simulate"
            )
        ),
        shiny.ui.panel_main(
            shiny.ui.output_plot("plot")
        )
    )
)

# Define the server logic
def server(input, output, session):
    @output
    @shiny.render.plot
    def plot():
        # Simulate random walk when the button is clicked
        input.simulate()  # Ensure reactivity

        # Number of steps
        n_steps = input.steps()
        
        # Generate steps: -1 or 1
        steps = np.random.choice([-1, 1], size=n_steps)
        
        # Compute the random walk by cumulative sum
        walk = np.cumsum(steps)
        
        # Create the plot
        plt.figure()
        plt.plot(walk)
        plt.title(f"Random Walk with {n_steps} Steps")
        plt.xlabel("Step")
        plt.ylabel("Position")
        plt.grid(True)

# Create the Shiny app
app = shiny.App(app_ui, server)

# Run the app
if __name__ == "__main__":
    app.run()
