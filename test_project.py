from project import twos_str_to_int, int_to_twos_str, get_int


def main():
    test_twos_str_to_int()
    test_int_to_twos_str()
    test_get_int()


def test_twos_str_to_int():
    assert twos_str_to_int('0000', 4) == 0
    assert twos_str_to_int('000001', 6) == 1
    assert twos_str_to_int('1111110', 7) == -2
    assert twos_str_to_int('000000000011', 12) == 3
    assert twos_str_to_int('0000000010000', 13) == 16
    assert twos_str_to_int('100001', 6) == -31


def test_int_to_twos_str():
    assert int_to_twos_str(0, 4) == '0000'
    assert int_to_twos_str(1, 6) == '000001'
    assert int_to_twos_str(-2, 7) == '1111110'
    assert int_to_twos_str(3, 12) == '000000000011'
    assert int_to_twos_str(16, 13) == '0000000010000'
    assert int_to_twos_str(-31, 6) == '100001'


def test_get_int():
    assert get_int('00000') == 0
    assert get_int('1') == 1
    assert get_int('10') == 10
    assert get_int('0xA') == 10
    assert get_int('10000') == 10000
    assert get_int('0xABC') == 2748
