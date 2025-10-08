import os
import json
import importlib.util
import tempfile

def test_benchmark_and_json_output():
    # Dynamically import the script as a module
    script_path = os.path.join(os.path.dirname(__file__), "main.py")
    spec = importlib.util.spec_from_file_location("main", script_path)
    main = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main)

    # Check that the all_results variable exists and is a list
    assert hasattr(main, "all_results")
    assert isinstance(main.all_results, list)
    assert len(main.all_results) > 0
    # Check structure of a result
    sample = main.all_results[0]
    assert "model" in sample and "sentence" in sample and "inference_time_ms" in sample

    # Simulate saving to JSON and reading back (open in text mode)
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w+", delete=False) as tmp:
        json.dump(main.all_results, tmp)
        tmp_path = tmp.name
    with open(tmp_path, "r") as f:
        loaded = json.load(f)
    assert isinstance(loaded, list)
    os.remove(tmp_path)
