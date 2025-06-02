"""
Main entry point for DEM processing.
"""
import time
from gbofe.models.dem_processor import DEMProcessor
from gbofe.algorithms.carve_method import RCarveMethod
from gbofe.algorithms.excavation_methods import NormalExcavationMethod, NormalExcavationModifiedMethod
from gbofe.algorithms.gbofe_method import GBOFEMethod
from gbofe.utils.ui_helpers import get_user_input
from gbofe.config import FlowEnforcementMethod
from gbofe.exceptions import DEMProcessingError

class FlowEnforcementFactory:
    """Factory to create flow enforcement strategies."""

    @staticmethod
    def create(method: FlowEnforcementMethod, gradient: float):
        """Creates the appropriate strategy based on the selected method."""
        strategy_map = {
            FlowEnforcementMethod.R_CARVE: RCarveMethod,
            FlowEnforcementMethod.NORMAL_EXCAVATION: NormalExcavationMethod,
            FlowEnforcementMethod.NORMAL_EXCAVATION_MODIFIED: NormalExcavationModifiedMethod,
            FlowEnforcementMethod.GBOFE: GBOFEMethod
        }

        strategy_class = strategy_map.get(method)
        if strategy_class is None:
            raise ValueError(f"Method not supported: {method}")

        return strategy_class(gradient)

def main():
    """Main program function."""
    try:
        # Get user parameters
        print("=== DEM Flow Enforcement Processor ===\n")

        dem_path, drainage_path, gradient, output_path, method, recursive = get_user_input()

        print(f"\nStarting processing with method: {method.name}")
        start_time = time.time()

        # Create processor
        processor = DEMProcessor.from_files(dem_path, drainage_path)

        # Create strategy
        strategy = FlowEnforcementFactory.create(method, gradient)

        # Process
        result = processor.process(strategy, recursive=recursive)

        # Save result
        result.save(output_path)

        # Show execution time
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"\n✅ Processing completed successfully!")
        print(f"📁 File saved in: {output_path}")
        print(f"⏱️  Execution time: {execution_time:.2f} seconds")

    except DEMProcessingError as e:
        print(f"❌ Error in processing: {e}")
    except KeyboardInterrupt:
        print("\n⚠️  Processing canceled by the user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()