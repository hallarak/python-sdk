# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from typing import Iterable as typing___Iterable
from typing import Optional as typing___Optional
from typing import Text as typing___Text

from google.protobuf.descriptor import Descriptor as google___protobuf___descriptor___Descriptor
from google.protobuf.descriptor import (
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)
from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
)
from google.protobuf.message import Message as google___protobuf___message___Message
from typing_extensions import Literal as typing_extensions___Literal

builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int

DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

class Http(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    fully_decode_reserved_expansion: builtin___bool = ...
    @property
    def rules(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        type___HttpRule
    ]: ...
    def __init__(
        self,
        *,
        rules: typing___Optional[typing___Iterable[type___HttpRule]] = None,
        fully_decode_reserved_expansion: typing___Optional[builtin___bool] = None,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "fully_decode_reserved_expansion",
            b"fully_decode_reserved_expansion",
            "rules",
            b"rules",
        ],
    ) -> None: ...

type___Http = Http

class HttpRule(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    selector: typing___Text = ...
    get: typing___Text = ...
    put: typing___Text = ...
    post: typing___Text = ...
    delete: typing___Text = ...
    patch: typing___Text = ...
    body: typing___Text = ...
    response_body: typing___Text = ...
    @property
    def custom(self) -> type___CustomHttpPattern: ...
    @property
    def additional_bindings(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        type___HttpRule
    ]: ...
    def __init__(
        self,
        *,
        selector: typing___Optional[typing___Text] = None,
        get: typing___Optional[typing___Text] = None,
        put: typing___Optional[typing___Text] = None,
        post: typing___Optional[typing___Text] = None,
        delete: typing___Optional[typing___Text] = None,
        patch: typing___Optional[typing___Text] = None,
        custom: typing___Optional[type___CustomHttpPattern] = None,
        body: typing___Optional[typing___Text] = None,
        response_body: typing___Optional[typing___Text] = None,
        additional_bindings: typing___Optional[typing___Iterable[type___HttpRule]] = None,
    ) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "custom",
            b"custom",
            "delete",
            b"delete",
            "get",
            b"get",
            "patch",
            b"patch",
            "pattern",
            b"pattern",
            "post",
            b"post",
            "put",
            b"put",
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "additional_bindings",
            b"additional_bindings",
            "body",
            b"body",
            "custom",
            b"custom",
            "delete",
            b"delete",
            "get",
            b"get",
            "patch",
            b"patch",
            "pattern",
            b"pattern",
            "post",
            b"post",
            "put",
            b"put",
            "response_body",
            b"response_body",
            "selector",
            b"selector",
        ],
    ) -> None: ...
    def WhichOneof(
        self, oneof_group: typing_extensions___Literal["pattern", b"pattern"]
    ) -> typing_extensions___Literal["get", "put", "post", "delete", "patch", "custom"]: ...

type___HttpRule = HttpRule

class CustomHttpPattern(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    kind: typing___Text = ...
    path: typing___Text = ...
    def __init__(
        self,
        *,
        kind: typing___Optional[typing___Text] = None,
        path: typing___Optional[typing___Text] = None,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions___Literal["kind", b"kind", "path", b"path"]
    ) -> None: ...

type___CustomHttpPattern = CustomHttpPattern
