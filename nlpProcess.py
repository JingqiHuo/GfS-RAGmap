import re
import spacy

class nlpProcess:
    def __init__(self, text):
        self.text = text
        self.nlp = spacy.load("en_core_web_trf")  # 推荐 en_core_web_trf 更强
        self.doc = self.nlp(text)

    def extract_coordinates(self):
        # 提取纬度经度并转换为负值（西经）
        coord_pattern = r'([0-9.]+)°N,\s*([0-9.]+)°W'
        matches = re.findall(coord_pattern, self.text)
        coords = [f"{lat},{-float(lon)}" for lat, lon in matches]
        return coords

    def extract_place_names(self):
        # 提取地名实体
        places = [ent.text.strip() for ent in self.doc.ents if ent.label_ in ["GPE", "LOC"]]
        return list(dict.fromkeys(places))  # 保留顺序去重

    def build_tasks(self, place_names, coords):
        tasks = []

        # 匹配地点与坐标（顺序简单对齐）
        for i, coord in enumerate(coords):
            name = place_names[i] if i < len(place_names) else f"Place {i+1}"
            tasks.append({
                "type": "point",
                "name": name,
                "coord": coord
            })

        # 构造 polyline（首尾点连线）
        if len(coords) >= 2:
            tasks.append({
                "type": "polyline",
                "origin": coords[0],
                "destination": coords[1]
            })

        # 构造 polygon（闭合）
        if len(coords) >= 3:
            tasks.append({
                "type": "polygon",
                "name": "Detected Area",
                "coords": coords + [coords[0]]
            })

        return tasks

    def process(self):
        coords = self.extract_coordinates()
        places = self.extract_place_names()
        tasks = self.build_tasks(places, coords)
        return tasks
