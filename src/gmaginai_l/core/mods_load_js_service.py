from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from pyjsparser import parse

logger = logging.getLogger(__name__)


class InvalidStructureError(Exception):
    pass


class ModsLoadJsService:
    def __init__(self):
        pass

    def to_dict(self, mods_load_js: str):
        ast = parse(mods_load_js)
        if ast["body"][0]["type"] == "VariableDeclaration":
            result = self._mods_load_js_json_to_dict_with_var(ast)
        elif ast["body"][0]["type"] == "ExpressionStatement":
            result = self._mods_load_js_json_to_dict_no_var(ast)
        else:
            raise InvalidStructureError("No VariableDeclaration or ExpressionStatement")

        return result

    def from_dict(self, mods_load_dict):
        mods_list = "\n".join([f"    '{mod}'," for mod in mods_load_dict["mods"]])

        template = """
LOADDATA = {{
  mods: [
    // enabled mods
{}
  ]
}};
        """.strip()
        return template.format(mods_list)

    def _get_mods_property(self, expression: dict):
        for prop in expression["properties"]:
            if prop["key"]["name"] == "mods":
                return prop

        return None

    def _object_expression_to_dict(self, object_expression):
        prop = self._get_mods_property(object_expression)
        if prop is None:
            raise InvalidStructureError(f"'mods' property not found")

        arrayexp_elements = prop["value"]["elements"]

        rtn_array = []

        for element in arrayexp_elements:
            if element["type"] == "Literal":
                rtn_array.append(str(element["value"]))

        rtn = {"mods": rtn_array}

        return rtn

    def _mods_load_js_json_to_dict_no_var(self, ast: dict):
        expression = ast["body"][0]
        assign = expression["expression"]
        object_expression = assign["right"]
        rtn = self._object_expression_to_dict(object_expression)
        return rtn

    def _mods_load_js_json_to_dict_with_var(self, ast: dict):
        declarations = ast["body"][0]["declarations"]
        object_expression = declarations[0]["init"]
        rtn = self._object_expression_to_dict(object_expression)
        return rtn
