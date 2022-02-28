import string
import uuid
import json
import datetime as dt
import dateutil
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List

from .utils import get_short_id


@dataclass
class Option:
    content: str
    is_correct: bool = False
    created_at: dt.datetime = field(default_factory=lambda: dt.datetime.utcnow())

    @property
    def uuid(self) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_OID, self.content))


@dataclass
class Question:
    question: str
    description: Optional[str] = None
    correct_choices: int = 1
    created_at: dt.datetime = field(
        default_factory=lambda: dt.datetime.utcnow()
    )
    options: List = field(
        default_factory=list
    )
    short_id: str = field(
        default_factory=get_short_id
    )

    @classmethod
    def _get_init_arglist(cls):
        import inspect
        return inspect.getfullargspec(cls).args

    class Encoder(json.JSONEncoder):
        def default(self, o: Any) -> Any:
            if isinstance(o, Question):
                return o.__dict__
            if isinstance(o, Option):
                return o.__dict__
            if isinstance(o, dt.datetime):
                return dt.datetime.strftime(o, "%Y-%m-%d %H:%M:%S")
            return json.JSONEncoder.default(self, o)

    class Decoder(json.JSONDecoder):

        def __init__(self, *args, **kwargs):
            super().__init__(object_hook=self.object_hook, *args, **kwargs)

        def object_hook(self, obj: Dict) -> Dict:
            attributes = set(Question._get_init_arglist())
            object_keys = set(obj.keys())
            # If not all attributes match; return dict object
            if attributes - object_keys - {"self"}:
                return obj
            # Return question-ready kwargs
            return {
                **obj,
                "created_at": dateutil.parser.parse(obj["created_at"]),
                "options": [
                    Option(**opt)
                    for opt in obj["options"]
                ]
            }

    @classmethod
    def from_payload(cls, payload: str, **kwargs) -> 'Question':
        instance_kwargs = json.loads(payload, cls=cls.Decoder)
        return cls(**instance_kwargs)

    @property
    def payload(self) -> str:
        return json.dumps(self, cls=self.Encoder)

    @property
    def uuid(self):
        return uuid.uuid5(uuid.NAMESPACE_OID, self.short_id)

    @property
    def option_hashtable(self) -> Dict[str, Option]:
        return {
            opt.uuid: opt
            for opt in self.options
        }

    @property
    def option_letter(self) -> Dict[str, str]:
        return {
            opt.uuid: string.ascii_uppercase[i]
            for i, opt in enumerate(self.options)
        }

    def get_option(self, opt_uuid: str) -> Optional[Option]:
        return self.option_hashtable.get(opt_uuid)

    def add_option(self, new_option: Option):
        self.options.append(new_option)

    def create_and_assign_option(self, content: str, is_correct: bool = False) -> Option:
        option = Option(content=content, is_correct=is_correct)
        self.add_option(new_option=option)
        return option

    def drop_option(self, uuid: str, *uuids: str):
        drop_list = [uuid, *uuids]
        self.options = [option for option in self.options if option.uuid not in drop_list]


@dataclass
class Answer:
    question: Question
    author: str = "anonymous"
    created_at: dt.datetime = field(
        default_factory=lambda: dt.datetime.utcnow()
    )
    options: List = field(
        default_factory=list
    )

    class Encoder(Question.Encoder):
        def default(self, o: Any) -> Any:
            if isinstance(o, Answer):
                return o.__dict__
            return super().default(o=o)

    @property
    def payload(self) -> str:
        return json.dumps(self, cls=self.Encoder)

    @property
    def uuid(self):
        return uuid.uuid5(uuid.NAMESPACE_OID, self.payload)
