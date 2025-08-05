from typing import Generic, TypeVar

InputType = TypeVar('InputType')
OutputType = TypeVar('OutputType')


class BaseController(Generic[InputType, OutputType]):
    def execute(self, input: InputType) -> OutputType:
        raise NotImplementedError("execute must be implemented by subclasses")
