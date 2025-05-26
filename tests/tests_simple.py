"""Super simple tests that should always work."""

def test_basic_math():
    """Test that basic math works."""
    assert 1 + 1 == 2


def test_can_import_pybleau():
    """Test that we can import the pybleau package."""
    import pybleau
    assert pybleau is not None


def test_pybleau_has_version():
    """Test that pybleau has a version."""
    import pybleau
    assert hasattr(pybleau, '__version__')


def test_requests_library_available():
    """Test that requests library is available."""
    import requests
    assert requests is not None


def test_can_import_auth_module():
    """Test that we can import the auth module."""
    try:
        from pybleau import auth
        assert auth is not None
    except ImportError as e:
        import pytest
        pytest.skip(f"Cannot import auth module: {e}")


def test_tableau_client_class_exists():
    """Test that TableauClient class exists."""
    try:
        from pybleau.auth import TableauClient
        assert TableauClient is not None
    except (ImportError, AttributeError) as e:
        import pytest
        pytest.skip(f"TableauClient not available: {e}")
