import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import os

st.set_page_config(page_title="Cannonball Sim", layout="wide")
st.title("3D Cannonball Simulation")

# 1. UI Inputs in the Sidebar
st.sidebar.header("Simulation Parameters")
v0 = st.sidebar.number_input("Initial Velocity (m/s)", min_value=1.0, value=50.0)
theta = st.sidebar.slider("Launch Angle (Theta - deg)", 0.0, 90.0, 45.0)
phi = st.sidebar.slider("Azimuth Angle (Phi - deg)", 0.0, 360.0, 90.0)
dt = st.sidebar.number_input("Time Step (dt)", value=0.01, format="%.3f")
total_time = st.sidebar.number_input("Max Flight Time (s)", value=10.0)

# Run button triggers the execution flow
if st.sidebar.button("Fire Cannon!"):

    # 2. Write parameters to config.txt
    with open("config.txt", "w") as f:
        f.write(f"{v0} {theta} {phi} {dt} {total_time}")

    # 3. Execute the C++ simulation using subprocess
    executable_path = "./cmake-build-debug/sim_executable"

    with st.spinner("Running C++ Physics Engine..."):
        try:
            # Run the C++ program and wait for it to finish
            subprocess.run([executable_path], check=True, capture_output=True, text=True)

            # 4. Read the output and visualize
            if os.path.exists("trajectory.csv"):
                df = pd.read_csv("trajectory.csv")

                # Plotting the data
                fig = plt.figure(figsize=(10, 6))
                ax = fig.add_subplot(111, projection='3d')

                # Note: We swap y and z so the height (y) is visually "up" on the graph
                ax.plot(df['x'], df['z'], df['y'], color='firebrick', linewidth=2.5)
                ax.set_xlabel('X Distance (m)')
                ax.set_ylabel('Z Depth (m)')
                ax.set_zlabel('Y Height (m)')

                st.pyplot(fig)

                st.success("Target hit! Trajectory rendered successfully.")
                # Display the raw data table below the graph
                st.subheader("Trajectory Data Table")
                st.dataframe(df, use_container_width=True)

            else:
                st.error("trajectory.csv was not found.")

        except FileNotFoundError:
            st.error(f"Could not find C++ executable at {executable_path}")
        except subprocess.CalledProcessError as e:
            st.error(f"C++ simulation crashed! Error: {e.stderr}")
