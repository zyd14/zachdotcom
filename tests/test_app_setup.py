
def test_setup_app_manual():
    from flask_app.mysite import create_app, RequestFormatter
    create_app()
    from flask.logging import default_handler
    
    assert isinstance(default_handler.formatter, RequestFormatter)
