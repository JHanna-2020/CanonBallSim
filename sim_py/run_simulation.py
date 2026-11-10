import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import os

st.set_page_config(page_title="Cannonball Sim", layout="wide")
st.title("3D Cannonball Simulation")

st.sidebar.header("Simulation Parameters")
v0 = st.sidebar.number_input("Initial Velocity (m/s)", min_value=1.0, value=50.0)
theta = st.sidebar.slider("Launch Angle (Theta - deg)", 0.0, 90.0, 45.0)
phi = st.sidebar.slider("Azimuth Angle (Phi - deg)", 0.0, 360.0, 90.0)
dt = st.sidebar.number_input("Time Step (dt)", min_value=0.001, value=0.01, format="%.3f")
total_time = st.sidebar.number_input("Max Flight Time (s)", min_value=0.1, value=10.0)

# Initialize Session State
if "df" not in st.session_state:
    st.session_state.df = None
if "error_msg" not in st.session_state:
    st.session_state.error_msg = None
if "landed" not in st.session_state:
    st.session_state.landed = False

if st.sidebar.button("Fire Cannon!"):
    # Clear previous state on new run
    st.session_state.error_msg = None
    st.session_state.df = None
    st.session_state.landed = False

    executable_path = "./cmake-build-debug/sim_executable"

    with st.spinner("Running C++ Physics Engine..."):
        try:
            if os.path.exists("trajectory.csv"):
                os.remove("trajectory.csv")

            with open("config.txt", "w") as f:
                f.write(f"{v0} {theta} {phi} {dt} {total_time}")

            result = subprocess.run([executable_path], check=True, capture_output=True, text=True, timeout=5)

            output_lines = result.stdout.splitlines()
            if "landed" in output_lines:
                st.session_state.landed = True
            elif "max_time" in output_lines:
                st.session_state.landed = False
            else:
                # Treat a missing status line as a firm error
                raise ValueError("C++ binary did not return a valid landing status.")

            if os.path.exists("trajectory.csv"):
                st.session_state.df = pd.read_csv("trajectory.csv")
            else:
                st.session_state.error_msg = "C++ ran, but trajectory.csv was not generated."

        except subprocess.TimeoutExpired:
            st.session_state.error_msg = "Simulation timed out! Check for infinite loops."
        except subprocess.CalledProcessError as e:
            st.session_state.error_msg = f"C++ simulation failed!\nError Output: {e.stderr}"
        # Added pd.errors.ParserError to catch ragged CSV rows
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            st.session_state.error_msg = "The generated trajectory.csv file is empty or corrupted."
        except OSError as e:
            st.session_state.error_msg = f"File or execution error: {e}"
        except ValueError as e:
            st.session_state.error_msg = str(e)

# Rendering Block
if st.session_state.error_msg:
    st.error(st.session_state.error_msg)

# Only show the success plot if there is no error sitting above it
elif st.session_state.df is not None:
    df = st.session_state.df

    # Catch 1-row flights before plotting
    if len(df) < 2:
        st.warning("No flight: fewer than two data points. Check the launch angle and time step.")
    else:
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(df['x'], df['z'], df['y'], color='firebrick', linewidth=2.5)

        span = max(df['x'].max() - df['x'].min(), df['z'].max() - df['z'].min(), df['y'].max(), 1.0)
        cx = (df['x'].max() + df['x'].min()) / 2
        cz = (df['z'].max() + df['z'].min()) / 2
        ax.set_xlim(cx - span/2, cx + span/2)
        ax.set_ylim(cz - span/2, cz + span/2)
        ax.set_zlim(0, span)

        ax.set_box_aspect([1, 1, 1])

        ax.set_xlabel('X Distance (m)')
        ax.set_ylabel('Z Depth (m)')
        ax.set_zlabel('Y Height (m)')

        st.pyplot(fig)

        if st.session_state.landed:
            st.success("Target hit! Trajectory rendered successfully.")
        else:
            # The empty df check is no longer needed here
            last_y = df.iloc[-1]['y']
            st.warning(f"Max flight time reached in mid-air! Ball was still {last_y:.1f}m high.")

        st.subheader("Trajectory Data Table")
        st.dataframe(df, width="stretch")
