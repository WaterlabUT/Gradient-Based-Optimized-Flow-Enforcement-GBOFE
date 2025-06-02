"""
Helper functions for the user interface.
"""
import sys
import time
import os
from typing import Tuple
from gbofe.config import FlowEnforcementMethod, METHOD_DESCRIPTIONS, SUPPORTED_RASTER_EXTENSIONS, SUPPORTED_VECTOR_EXTENSIONS
from gbofe.utils.file_operations import validate_file_path, create_output_directory

def animated_loading(message: str) -> None:
    """
    Shows a loading animation for the user.

    Args:
        message: Message to display during loading
    """
    for _ in range(3):
        for dots in ['', '.', '..', '...']:
            sys.stdout.write(f'\r{message}{dots}')
            sys.stdout.flush()
            time.sleep(0.5)
    print()

def display_method_menu() -> None:
    """Displays the menu of available methods."""
    print("Available flow correction methods:")
    for method in FlowEnforcementMethod:
        print(f"{method.value}: {METHOD_DESCRIPTIONS[method]}")
    print()

def get_user_input() -> Tuple[str, str, float, str, FlowEnforcementMethod, bool]:
    """
    Requests the necessary parameters from the user.

    Returns:
        Tuple with validated parameters
    """
    # Selection of method
    display_method_menu()
    while True:
        try:
            method_choice = int(input('Choose the flow correction method: '))
            method = FlowEnforcementMethod(method_choice)
            break
        except (ValueError, KeyError):
            print("Invalid option. Please select a number from 1 to 4.")

    # DEM path
    while True:
        try:
            dem_path = input('Enter the DEM file path: ').strip('"').strip("'")
            dem_path = os.path.normpath(dem_path)
            validate_file_path(dem_path, SUPPORTED_RASTER_EXTENSIONS)
            break
        except Exception as e:
            print(f"Error: {e}")

    # Drainage path
    while True:
        try:
            drainage_path = input('Enter the drainage file path: ').strip('"').strip("'")
            drainage_path = os.path.normpath(drainage_path)
            validate_file_path(drainage_path, SUPPORTED_VECTOR_EXTENSIONS)
            break
        except Exception as e:
            print(f"Error: {e}")

    # Gradient
    while True:
        try:
            if method in [FlowEnforcementMethod.R_CARVE,
                          FlowEnforcementMethod.NORMAL_EXCAVATION,
                          FlowEnforcementMethod.NORMAL_EXCAVATION_MODIFIED]:
                gradient = float(input('Enter the excavation depth in meters: '))
            else:
                gradient = float(input('Enter the slope reduction gradient (G) {G > 0}: '))

            if gradient <= 0:
                print("The gradient must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    # Determine if it is recursive
    recursive = method in [FlowEnforcementMethod.NORMAL_EXCAVATION_MODIFIED,
                           FlowEnforcementMethod.GBOFE]

    # Path to the output file
    while True:
        try:
            output_path = input('Enter the output path for the corrected DEM: ').strip('"').strip("'")
            output_path = os.path.normpath(output_path)
            create_output_directory(output_path)
            break
        except Exception as e:
            print(f"Error creating directory: {e}")

    return dem_path, drainage_path, gradient, output_path, method, recursive