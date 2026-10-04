from tools import calculate_monthly_salary, get_company_rules


def test_technova_rules():
    result = get_company_rules("TechNova")
    assert result["found"] is True
    assert result["max_backlogs"] == 1
    assert result["min_cgpa"] == 7.0


def test_unknown_company():
    result = get_company_rules("UnknownCompany")
    assert result["found"] is False


def test_salary():
    result = calculate_monthly_salary(6)
    assert result["annual_rupees"] == 600000
    assert result["monthly_gross_rupees"] == 50000


def test_negative_salary():
    try:
        calculate_monthly_salary(-1)
        assert False
    except ValueError:
        assert True
