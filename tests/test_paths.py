from ds.paths import RAW_DATA_DIR, ROOT_DIR


def test_paths_exist():
    """Test that critical project paths exist."""
    assert ROOT_DIR.exists()
    assert RAW_DATA_DIR.exists()
    assert (ROOT_DIR / "pyproject.toml").exists()
