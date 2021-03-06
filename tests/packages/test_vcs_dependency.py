import pytest

from poetry.core.packages.vcs_dependency import VCSDependency


def test_to_pep_508():
    dependency = VCSDependency(
        "poetry", "git", "https://github.com/python-poetry/poetry.git"
    )

    expected = "poetry @ git+https://github.com/python-poetry/poetry.git@master"

    assert expected == dependency.to_pep_508()


def test_to_pep_508_ssh():
    dependency = VCSDependency("poetry", "git", "git@github.com:sdispater/poetry.git")

    expected = "poetry @ git+ssh://git@github.com/sdispater/poetry.git@master"

    assert expected == dependency.to_pep_508()


def test_to_pep_508_with_extras():
    dependency = VCSDependency(
        "poetry", "git", "https://github.com/python-poetry/poetry.git"
    )
    dependency.extras.append("foo")

    expected = "poetry[foo] @ git+https://github.com/python-poetry/poetry.git@master"

    assert expected == dependency.to_pep_508()


def test_to_pep_508_in_extras():
    dependency = VCSDependency(
        "poetry", "git", "https://github.com/python-poetry/poetry.git"
    )
    dependency.in_extras.append("foo")

    expected = 'poetry @ git+https://github.com/python-poetry/poetry.git@master ; extra == "foo"'
    assert expected == dependency.to_pep_508()

    dependency = VCSDependency(
        "poetry", "git", "https://github.com/python-poetry/poetry.git"
    )
    dependency.in_extras.append("foo")
    dependency.extras.append("bar")

    expected = 'poetry[bar] @ git+https://github.com/python-poetry/poetry.git@master ; extra == "foo"'

    assert expected == dependency.to_pep_508()

    dependency = VCSDependency(
        "poetry", "git", "https://github.com/python-poetry/poetry.git", "b;ar;"
    )
    dependency.in_extras.append("foo;")

    expected = 'poetry @ git+https://github.com/python-poetry/poetry.git@b;ar; ; extra == "foo;"'

    assert expected == dependency.to_pep_508()


@pytest.mark.parametrize("category", ["main", "dev"])
def test_category(category):
    dependency = VCSDependency(
        "poetry",
        "git",
        "https://github.com/python-poetry/poetry.git",
        category=category,
    )
    assert category == dependency.category
