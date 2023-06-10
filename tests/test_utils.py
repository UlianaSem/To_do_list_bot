import src.utils


def test_get_processed_date():
    assert src.utils.get_processed_date('2 сентября 2022') == '2022-09-02'
    assert src.utils.get_processed_date('02 сентября 2022') == '2022-09-02'
    assert src.utils.get_processed_date('02.09.2022') == '2022-09-02'
    assert src.utils.get_processed_date('2.09.2022') == '2022-09-02'
    assert src.utils.get_processed_date('02/09/2022') == '2022-09-02'
    assert src.utils.get_processed_date('2/09/2022') == '2022-09-02'
    assert src.utils.get_processed_date('02:09:2022') == '2022-09-02'
    assert src.utils.get_processed_date('2:09:2022') == '2022-09-02'
