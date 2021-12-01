from dataclasses import dataclass
from datetime import datetime


@dataclass
class DiaryRecord():
    id: int
    user_id: int
    record_text: str
    record_date: datetime

    def __init__(self, record_tuple: tuple):
        self.id = record_tuple[0]
        self.user_id = record_tuple[1]
        self.record_text = record_tuple[2]
        self.record_date = record_tuple[3]
    
    def __str__(self) -> str:
        return f"Запись № {self.id}: дата-{self.record_date}, пользователь id-{self.user_id}"

current_record: DiaryRecord = None