from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("name", "email", "age", "hobbies")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    HOBBIES_FIELD_NUMBER: _ClassVar[int]
    name: str
    email: str
    age: int
    hobbies: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., email: _Optional[str] = ..., age: _Optional[int] = ..., hobbies: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateUserRequest(_message.Message):
    __slots__ = ("name", "email", "age", "hobbies")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    HOBBIES_FIELD_NUMBER: _ClassVar[int]
    name: str
    email: str
    age: int
    hobbies: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., email: _Optional[str] = ..., age: _Optional[int] = ..., hobbies: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateUserResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: User
    def __init__(self, data: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: User
    def __init__(self, data: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class GetUsersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetUsersResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, data: _Optional[_Iterable[_Union[User, _Mapping]]] = ...) -> None: ...
