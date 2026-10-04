from typing import Any

COMPANY_RULES = {
    "technova": {
        "display_name": "TechNova",
        "max_backlogs": 1,
        "min_cgpa": 7.0,
        "eligible_branches": ["CSE", "IT", "ECE"],
    },
    "alphasoft": {
        "display_name": "AlphaSoft",
        "max_backlogs": 3,
        "min_cgpa": 7.5,
        "eligible_branches": ["CSE", "IT"],
    },
    "dataworks": {
        "display_name": "DataWorks",
        "max_backlogs": 0,
        "min_cgpa": 8.0,
        "eligible_branches": ["CSE", "IT", "ECE"],
    },
}


def get_company_rules(company: str) -> dict[str, Any]:
    """Retrieve placement eligibility rules for a company.

    Args:
        company: Company name.

    Returns:
        The company's eligibility rules or an unavailable message.
    """
    key = company.strip().lower()

    if key not in COMPANY_RULES:
        return {
            "found": False,
            "company": company,
            "message": "Company rules are not available in the current system."
        }

    rule = COMPANY_RULES[key]

    return {
        "found": True,
        "company": rule["display_name"],
        "max_backlogs": rule["max_backlogs"],
        "min_cgpa": rule["min_cgpa"],
        "eligible_branches": rule["eligible_branches"],
    }


def calculate_monthly_salary(lpa: float) -> dict[str, Any]:
    """Calculate approximate monthly gross salary from LPA.

    Args:
        lpa: Annual package in lakhs per annum.

    Returns:
        Annual salary and approximate monthly gross equivalent.
    """
    lpa = float(lpa)

    if lpa < 0:
        raise ValueError("LPA cannot be negative.")

    annual_rupees = lpa * 100000
    monthly_rupees = annual_rupees / 12

    return {
        "lpa": lpa,
        "annual_rupees": annual_rupees,
        "monthly_gross_rupees": round(monthly_rupees, 2),
        "note": "This is a simple gross monthly equivalent, not take-home salary."
    }


AVAILABLE_TOOLS = {
    "get_company_rules": get_company_rules,
    "calculate_monthly_salary": calculate_monthly_salary,
}
