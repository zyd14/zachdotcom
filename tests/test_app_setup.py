
def test_setup_app_manual():
    from mysite.app import create_app, RequestFormatter
    create_app()
    from flask.logging import default_handler
    
    assert isinstance(default_handler.formatter, RequestFormatter)
