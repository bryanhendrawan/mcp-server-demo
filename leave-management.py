# requirements:
# pip install fastmcp uvicorn

from mcp.server.fastmcp import FastMCP
from datetime import datetime
import uuid

# Create MCP server
mcp = FastMCP("Employee Leave Chat MCP")

# -------------------------------------------------------------------
# MOCK DUMMY DATA
# -------------------------------------------------------------------

employees = {
    "EMP001": {
        "name": "Bryan Hendrawan",
        "department": "Engineering",
        "position": "Software Engineer",
        "email": "bryan.hendrawan@company.com",
        "phone": "+62-812-0000-0001",
        "leave_balance": {
            "annual": 12,
            "sick": 8,
            "unpaid": 999,
        },
    },
    "EMP002": {
        "name": "John Doe",
        "department": "Finance",
        "position": "Financial Analyst",
        "email": "john.doe@company.com",
        "phone": "+62-812-0000-0002",
        "leave_balance": {
            "annual": 5,
            "sick": 2,
            "unpaid": 999,
        },
    },
}

leave_history = {
    "EMP001": [
        {
            "leave_id": "LV-1001",
            "type": "annual",
            "start_date": "2026-01-10",
            "end_date": "2026-01-12",
            "days": 3,
            "status": "approved",
            "reason": "Family vacation",
        },
        {
            "leave_id": "LV-1002",
            "type": "sick",
            "start_date": "2026-02-01",
            "end_date": "2026-02-01",
            "days": 1,
            "status": "approved",
            "reason": "Fever",
        },
    ],
    "EMP002": [],
}


# -------------------------------------------------------------------
# TOOL 1 - GET LEAVE BALANCE
# -------------------------------------------------------------------

@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """
    Get employee leave balance in chat-friendly format.
    """

    employee = employees.get(employee_id)

    if not employee:
        return f"❌ Employee ID {employee_id} not found."

    balances = employee["leave_balance"]

    return f"""
📋 Employee Leave Balance

Employee ID : {employee_id}
Name        : {employee['name']}
Department  : {employee['department']}

Remaining Leave:
- Annual Leave : {balances['annual']} days
- Sick Leave   : {balances['sick']} days
- Unpaid Leave : {balances['unpaid']} days
""".strip()


# -------------------------------------------------------------------
# TOOL 2 - GET LEAVE HISTORY
# -------------------------------------------------------------------

@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """
    Get employee leave history in chat-friendly format.
    """

    employee = employees.get(employee_id)

    if not employee:
        return f"❌ Employee ID {employee_id} not found."

    history = leave_history.get(employee_id, [])

    if not history:
        return f"""
📋 Leave History

Employee : {employee['name']}

No leave history found.
""".strip()

    result = f"""
📋 Leave History

Employee ID : {employee_id}
Employee    : {employee['name']}

""".strip()

    for idx, item in enumerate(history, start=1):
        result += f"""

{idx}. {item['type'].upper()} LEAVE
   Leave ID : {item['leave_id']}
   Date     : {item['start_date']} to {item['end_date']}
   Days     : {item['days']}
   Status   : {item['status']}
   Reason   : {item['reason']}
"""

    return result.strip()


# -------------------------------------------------------------------
# TOOL 3 - APPLY LEAVE
# -------------------------------------------------------------------

@mcp.tool()
def apply_leave(
    employee_id: str,
    leave_type: str,
    start_date: str,
    end_date: str,
    days: int,
    reason: str,
) -> str:
    """
    Apply employee leave and return chat-friendly response.
    """

    employee = employees.get(employee_id)

    if not employee:
        return f"❌ Employee ID {employee_id} not found."

    balances = employee["leave_balance"]

    if leave_type not in balances:
        return f"❌ Invalid leave type: {leave_type}"

    current_balance = balances[leave_type]

    if current_balance < days:
        return f"""
❌ Leave Application Failed

Employee : {employee['name']}
Leave Type : {leave_type}

Requested : {days} days
Available : {current_balance} days
""".strip()

    # deduct balance
    balances[leave_type] -= days

    # generate leave id
    leave_id = f"LV-{uuid.uuid4().hex[:8].upper()}"

    new_leave = {
        "leave_id": leave_id,
        "type": leave_type,
        "start_date": start_date,
        "end_date": end_date,
        "days": days,
        "status": "pending",
        "reason": reason,
        "applied_at": datetime.utcnow().isoformat(),
    }

    if employee_id not in leave_history:
        leave_history[employee_id] = []

    leave_history[employee_id].append(new_leave)

    return f"""
✅ Leave Application Submitted

Employee ID : {employee_id}
Employee    : {employee['name']}

Leave Details
--------------
Leave ID    : {leave_id}
Leave Type  : {leave_type}
Date        : {start_date} to {end_date}
Total Days  : {days}
Reason      : {reason}

Status      : pending

Remaining {leave_type} balance:
{balances[leave_type]} days
""".strip()


# -------------------------------------------------------------------
# TOOL 4 - GET EMPLOYEE INFO
# -------------------------------------------------------------------

@mcp.tool()
def get_employee_info(employee_id: str) -> str:
    """
    Get full employee profile in chat-friendly format.
    """

    employee = employees.get(employee_id)

    if not employee:
        return f"❌ Employee ID {employee_id} not found."

    return f"""
📋 Employee Information

Employee ID : {employee_id}
Name        : {employee['name']}
Department  : {employee['department']}
Position    : {employee['position']}
Email       : {employee['email']}
Phone       : {employee['phone']}
""".strip()


# -------------------------------------------------------------------
# TOOL 5 - HEALTH CHECK
# -------------------------------------------------------------------

@mcp.tool()
def health_check() -> str:
    """
    Health check endpoint.
    """

    return """
✅ Employee Leave Chat MCP is running successfully.
""".strip()

# -------------------------------------------------------------------
# RESOURCE - LEAVE POLICY
# -------------------------------------------------------------------
@mcp.resource("policy://leave")
def get_leave_policy() -> str:
    """
    Returns the company leave policy as a static reference document.
    """

    return """📋 Company Leave Policy

Leave Types & Entitlements:
- Annual Leave  : 12 days per year
- Sick Leave    : 8 days per year
- Unpaid Leave  : Unlimited (subject to approval)

Rules:
- Annual leave must be applied at least 3 days in advance.
- Sick leave requires a medical certificate for absences over 2 consecutive days.
- Unpaid leave requires manager and HR approval.
- Leave balances reset every January 1st.
- Unused annual leave can be carried over up to a maximum of 5 days.

Application Process:
1. Submit leave request via the HR system.
2. Manager approves or rejects within 2 business days.
3. Approved leave is reflected in your balance immediately.

Contact HR at hr@company.com for any queries.
""".strip()

# -------------------------------------------------------------------
# PROMPT - LEAVE APPLICATION PROMPT
# -------------------------------------------------------------------
@mcp.prompt()
def leave_application_prompt(employee_id: str, leave_type: str) -> str:
    """
    Generate a leave application prompt for the user.
    """

    employee = employees.get(employee_id)

    if not employee:
        return f"❌ Employee ID {employee_id} not found."

    return f"""📋 Leave Application Prompt
Employee : {employee['name']}
Leave Type : {leave_type}
Please provide the following details to apply for leave:
- Start Date (YYYY-MM-DD)
- End Date (YYYY-MM-DD)
- Total Days
- Reason for leave
""".strip()

# -------------------------------------------------------------------
# RUN SERVER
# -------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
    )