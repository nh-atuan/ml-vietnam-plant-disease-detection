"""
Expert Knowledge Base — Gợi ý xử lý bệnh theo luật chuyên gia.

Phụ trách: Lê Xuân Trí (Sáng tạo S3)
Phase 5, Task 5.4

TODO:
- [ ] Load disease database từ diseases.json
- [ ] Tra bảng nhãn → trả về mô tả bệnh + biện pháp xử lý (tiếng Việt)
- [ ] Cung cấp hành động cụ thể cho nông dân
- [ ] Tích hợp vào API response của FastAPI
"""

import json
import os
from typing import Dict, Any, Optional


# Đường dẫn đến file dữ liệu bệnh
DISEASES_DB_PATH = os.path.join(os.path.dirname(__file__), "diseases.json")


class KnowledgeBase:
    """
    Module tra cứu thông tin bệnh cây trồng.

    Cung cấp:
    - Tên bệnh (tiếng Việt + tiếng Anh)
    - Mô tả triệu chứng
    - Nguyên nhân gây bệnh
    - Biện pháp xử lý / phòng ngừa
    - Mức độ nghiêm trọng
    """

    def __init__(self, db_path: str = DISEASES_DB_PATH):
        # TODO: Load diseases.json
        raise NotImplementedError

    def get_disease_info(self, disease_label: str) -> Optional[Dict[str, Any]]:
        """
        Tra cứu thông tin bệnh theo nhãn dự đoán.

        Args:
            disease_label: Nhãn bệnh từ model (vd: "BrownSpot", "LeafBlast")

        Returns:
            Dict chứa: name_vi, name_en, description, symptoms,
                       causes, treatments, severity, prevention
        """
        # TODO: Implement lookup
        raise NotImplementedError

    def format_recommendation(self, disease_label: str, confidence: float) -> Dict[str, Any]:
        """
        Format gợi ý xử lý để trả về cho frontend.

        Args:
            disease_label: Nhãn bệnh
            confidence: Độ tin cậy dự đoán

        Returns:
            Dict sẵn sàng serialize JSON cho API response
        """
        # TODO: Implement
        raise NotImplementedError
