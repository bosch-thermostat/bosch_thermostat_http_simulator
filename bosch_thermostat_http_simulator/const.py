"""Const to use in bosch_simulator."""

ID = "id"
WRITEABLE = "writeable"
VALUE = "value"
ALLOWED_VALUES = "allowedValues"
NEFIT = "nefit"
IVT = "ivt"
EASYCONTROL = "easycontrol"

IVT_MAGIC = bytearray.fromhex(
    "867845e97c4e29dce522b9a7d3a3e07b152bffadddbed7f5ffd842e9895ad1e4"
)

NEFIT_MAGIC = bytearray.fromhex(
    "58f18d70f667c9c79ef7de435bf0f9b1553bbb6e61816212ab80e5b0d351fbb1"
)

EASYCONTROL_MAGIC = bytearray.fromhex(
    "1d86b2631b02f2c7978b41e8a3ae609b0b2afbfd30ff386da60c586a827408e4"
)

MAGICS = {IVT: IVT_MAGIC, NEFIT: NEFIT_MAGIC, EASYCONTROL: EASYCONTROL_MAGIC}
