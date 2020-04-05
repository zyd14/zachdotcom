from flask_app.mysite import fakestuff

def test_get_df():
    df = fakestuff.mock_garden_log()
    assert len(df) > 0
