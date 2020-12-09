import json
from typing import Any, Dict, List, Optional, Union

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict

message_map = lambda view: lambda status_code: {  # noqa
    "POST": "%s created successfully" % view.name.capitalize(),
    "PATCH": "%s updated succesfully" % view.name.capitalize(),
    "DELETE": "%s deleted successfully" % view.name.capitalize(),
}.get(status_code)


class UserJSONRenderer(JSONRenderer):
    """
    Renderer which serializes data to JSON.
    """

    charset = "utf-8"

    def render(
        self,
        data: Union[
            Dict[str, ErrorDetail],
            ReturnDict,
            Dict[str, Union[str, List[ErrorDetail]]],
            Dict[str, Union[str, Dict[str, str]]],
            Dict[str, str],
        ],
        media_type: Optional[str] = None,
        renderer_context: Optional[Dict[str, Any]] = None,
    ) -> Union[str, bytes]:
        if renderer_context["response"].status_code == 422:
            renderer_context["response"].status_code = status.HTTP_400_BAD_REQUEST
        status_code = renderer_context["response"].status_code

        return (
            json.dumps(data)
            if status.is_success(status_code)
            else super(UserJSONRenderer, self).render(
                {
                    "message": data.pop("message", "Fix the error(s) below"),
                    "errors": data,
                }
            )
        )