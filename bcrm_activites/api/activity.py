import frappe
import json

@frappe.whitelist()
def get_activity(doctype, docname):

    versions = frappe.get_all(

        "Version",

        filters={

            "ref_doctype": doctype,
            "docname": docname

        },

        fields=[

            "owner",
            "creation",
            "data"

        ],

        order_by="creation desc",

        limit=100
    )

    result = []

    for row in versions:

        try:

            data = json.loads(
                row.data or "{}"
            )

        except Exception:

            data = {}

        changes = []

        # =========================================
        # CHANGED FIELDS
        # =========================================

        for d in data.get("changed", []):

            try:

                changes.append({

                    "field":
                        format_field(
                            d[0]
                        ),

                    "old":
                        str(d[1] or "--"),

                    "new":
                        str(d[2] or "--")
                })

            except:

                pass

        # =========================================
        # USER DETAILS
        # =========================================

        user = frappe.db.get_value(

            "User",
            row.owner,

            [
                "full_name",
                "user_image"
            ],

            as_dict=True
        )

        result.append({

            "user":
                row.owner,

            "full_name":
                (
                    user.full_name
                    if user
                    else row.owner
                ),

            "user_image":
                (
                    user.user_image
                    if user
                    else ""
                ),

            "time":
                row.creation,

            "changes":
                changes
        })

    return result


# =============================================
# FORMAT FIELD
# =============================================

def format_field(fieldname):

    if not fieldname:

        return ""

    return (

        fieldname
        .replace("_", " ")
        .title()

    )