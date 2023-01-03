import dataclasses
from typing import List

from marshmallow import Schema, fields, post_load
from pydantic import BaseModel


@dataclasses.dataclass
class SaveFeedbackDto:

    def __init__(self, feedback, community_name, community_size):
        self.feedback = feedback
        self.community_name = community_name
        self.community_size = community_size





