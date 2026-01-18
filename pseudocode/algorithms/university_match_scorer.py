# 院校匹配评分器实现代码
# 文件路径: algorithms/university_match_scorer.py

from typing import Dict, Any, List


class UniversityMatchScorer:
    """University match scorer"""

    XI_AN_UNIVERSITIES = {
        "西安交通大学": {
            "domain": [
                "engineering",
                "computer",
                "technology",
                "mechanical",
                "materials",
            ],
            "keywords": ["innovation", "robotics", "aerospace", "energy"],
        },
        "西北工业大学": {
            "domain": ["aeronautics", "materials", "marine", "computer"],
            "keywords": ["design", "simulation", "testing"],
        },
        "西安电子科技大学": {
            "domain": ["electronics", "communication", "information", "technology"],
            "keywords": [
                "integrated circuit",
                "microchip",
                "semiconductor",
                "signal processing",
            ],
        },
        "西北大学": {
            "domain": [
                "archaeology",
                "history",
                "literature",
                "philosophy",
                "economics",
            ],
            "keywords": ["cultural heritage", "ancient", "research methodology"],
        },
    }

    MAJOR_KEYWORDS = {
        "计算机科学与技术": [
            "computer",
            "programming",
            "algorithm",
            "software",
            "data",
            "network",
            "AI",
            "machine learning",
        ],
        "电子工程": ["circuit", "chip", "hardware", "embedded", "VLSI", "FPGA"],
        "机械工程": [
            "mechanical",
            "design",
            "CAD",
            "manufacturing",
            "materials",
            "robotics",
        ],
        "材料科学": [
            "materials",
            "properties",
            "nanotechnology",
            "polymer",
            "composite",
            "metallurgy",
        ],
    }

    def calculate_match_score(
        self, answer: str, university: str, major: str
    ) -> Dict[str, Any]:
        """Calculate university match score.

        Args:
            answer: Answer text
            university: Target university
            major: Target major

        Returns:
            Dict containing match details
        """
        words = answer.lower().split()

        domain_match_score = self._match_university_domain(words, university)
        major_match_score = self._match_major_domain(words, major)
        matched_keywords = self._extract_matched_keywords(words, university, major)

        overall_score = round((domain_match_score + major_match_score) / 2, 2)
        relevance = self._determine_relevance(overall_score)

        suggestions = []
        if overall_score < 60:
            suggestions.append(
                f"Try to incorporate more vocabulary related to {university} and {major}"
            )
        elif overall_score < 80:
            suggestions.append(
                f"Good start! Try to add more specific details about {major}"
            )
        else:
            suggestions.append(
                f"Excellent answer that aligns well with {university}'s {major} program!"
            )

        return {
            "score": overall_score,
            "relevance": relevance,
            "matched_keywords": matched_keywords,
            "domain_match_score": domain_match_score,
            "major_match_score": major_match_score,
            "suggestions": suggestions,
        }

    def _match_university_domain(self, words: List[str], university: str) -> float:
        """Match university domain keywords."""
        university_info = self.XI_AN_UNIVERSITIES.get(
            university, {"domain": [], "keywords": []}
        )
        domain_keywords = set([kw.lower() for kw in university_info["domain"]])

        words_lower = [w.lower() for w in words]
        matches = sum(1 for w in words_lower if w in domain_keywords)

        if not words:
            return 0

        match_ratio = matches / len(words)
        return min(100, match_ratio * 100)

    def _match_major_domain(self, words: List[str], major: str) -> float:
        """Match major domain keywords."""
        major_keywords = set([kw.lower() for kw in self.MAJOR_KEYWORDS.get(major, [])])

        words_lower = [w.lower() for w in words]
        matches = sum(1 for w in words_lower if any(kw in w for kw in major_keywords))

        if not words:
            return 0

        match_ratio = matches / len(words)
        return min(100, match_ratio * 100)

    def _extract_matched_keywords(
        self, words: List[str], university: str, major: str
    ) -> List[str]:
        """Extract matched keywords."""
        university_info = self.XI_AN_UNIVERSITIES.get(university, {"keywords": []})
        major_info = self.MAJOR_KEYWORDS.get(major, [])

        all_keywords = set(university_info["keywords"] + major_info)

        words_lower = [w.lower() for w in words]
        matched = [w for w in words_lower if w in all_keywords]

        return matched

    def _determine_relevance(self, score: float) -> str:
        """Determine relevance level."""
        if score >= 85:
            return "high"
        elif score >= 70:
            return "medium"
        elif score >= 50:
            return "low"
        else:
            return "none"
