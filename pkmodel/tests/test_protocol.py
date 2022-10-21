import numpy.testing as npt
import pytest

@pytest.mark.parameterize(
    'test expected',
    [
        ('')
    ]
)
def test_type_of_dosis():
