import importlib.util
import random

def test_sentiment_analysis_pipeline():
    # Dynamically import the script as a module
    script_path = __import__('os').path.join(__import__('os').path.dirname(__file__), "main.py")
    spec = importlib.util.spec_from_file_location("main", script_path)
    main = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main)

    # Check that the sentiment_analyzer exists
    assert hasattr(main, "sentiment_analyzer")
    # Check that the dataset is loaded
    assert hasattr(main, "all_data")
    assert len(main.all_data) > 0
    # Check that sample_reviews is a list of length 5
    assert hasattr(main, "sample_reviews")
    assert len(main.sample_reviews) == 5
    # Check that each review has a 'review' field
    for review in main.sample_reviews:
        assert "review" in review
        result = main.sentiment_analyzer(review["review"][:512])
        assert isinstance(result, list)
        assert "label" in result[0] and "score" in result[0]

