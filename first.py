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



# def plot():
#     # Simulate random walk when the button is clicked
#     input.simulate()  # Ensure reactivity

#     # Number of steps
#     n_steps = input.steps()
    
#     # Generate steps: -1 or 1
#     steps = np.random.choice([-1, 1], size=n_steps)
    
#     # Compute the random walk by cumulative sum
#     walk = np.cumsum(steps)
    
#     # Create the plot
#     plt.figure()
#     plt.plot(walk)
#     plt.title(f"Random Walk with {n_steps} Steps")
#     plt.xlabel("Step")
#     plt.ylabel("Position")
#     plt.grid(True)

# Define the server logic
def server(input, output, session):
    @output
    @shiny.render.plot
    def plot():
        # Simulate random walk when the button is clicked
        input.simulate()  # Ensure reactivity
        plt.rcParams['figure.facecolor'] = 'black' 

        ## Random walk, but in polar co-ordinates.
        ## Also the random walk in r and theta axes are completely independent (unlike the x-y co-ordinate system)

        n_steps = input.steps()
        del_theta=1/10                    ##step size for angle
        del_r=1                           ##step size for radius

        r=np.zeros(n_steps)
        theta=np.zeros(n_steps)
        Z= np.zeros(n_steps,dtype='complex128')
        Z[0]=0
        theta=0
        r=0
        np.random.seed(0)
        # for i in range(1, n_steps):
            
        #     k_r=np.random.choice(a=np.arange(3)-1,p=[0.25,0.25,0.5])     ## biased RW to throu the particle in one direction
        #     k_theta=np.random.choice(a=np.arange(3)-1,p=[0.25,0.25,0.5]) ## biased RW to make a spiral structure
        #     r+=del_r*k_r
        #     theta+=del_theta*k_theta
        #     Z[i]=1*r*np.exp(1j*theta)
        # Generate random choices for k_r and k_theta for all steps at once
        k_r = np.random.choice(a=np.arange(3)-1, p=[0.25, 0.25, 0.5], size=n_steps-1)
        k_theta = np.random.choice(a=np.arange(3)-1, p=[0.25, 0.25, 0.5], size=n_steps-1)
        r_values = np.cumsum(np.concatenate(([r], del_r * k_r)))
        theta_values = np.cumsum(np.concatenate(([theta], del_theta * k_theta)))
        Z = r_values * np.exp(1j * theta_values)
        # If the first value of Z should be 0, adjust as needed
        Z[0] = 1 * r * np.exp(1j * theta)
            
        plt.figure(figsize=(10,10))
        plt.scatter(Z.real,Z.imag,s=1,color='w')                        ##scatter plot the point.  's' specifies the markersize
        plt.axis('equal')
        plt.axis('off')

# Create the Shiny app
app = shiny.App(app_ui, server)

# Run the app
if __name__ == "__main__":
    app.run()
