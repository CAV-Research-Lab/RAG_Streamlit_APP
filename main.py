import subprocess
import sys
import os

def run_streamlit_app():
    try:
        # Define the absolute path to the directory containing app.py
        project_dir = os.path.dirname(__file__)
        app_path = os.path.join(project_dir, "app.py")

        # Check if the app.py file exists
        if not os.path.exists(app_path):
            raise FileNotFoundError(f"File not found: {app_path}")

        # Set the working directory to the project's directory
        os.chdir(project_dir)

        # Run the Streamlit app using subprocess
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
    except FileNotFoundError as e:
        print(e)
    except KeyboardInterrupt:
        print("Streamlit application interrupted by the user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_streamlit_app()
