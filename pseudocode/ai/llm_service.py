# LLM服务伪代码
# 文件路径: ai/llm_service.py

from typing import Dict, Any, List, Optional
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage


class LLMService:
    """LLM服务"""

    def __init__(
        self,
        model_name: str = "qwen2.5-7b",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        初始化LLM服务

        Args:
            model_name: 模型名称
            api_key: API密钥
            base_url: API基础URL
        """
        self.model_name = model_name

        # 初始化LLM
        self.llm = ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=0.7,
            max_tokens=1000
        )

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        对话

        Args:
            messages: 消息列表

        Returns:
            回复内容
        """
        # 转换消息格式
        langchain_messages = []
        for msg in messages:
            if msg["role"] == "system":
                langchain_messages.append(SystemMessage(content=msg["content"]))
            else:
                langchain_messages.append(HumanMessage(content=msg["content"]))

        # 调用LLM
        response = self.llm(langchain_messages)
        return response.content

    def generate_question(
        self,
        context: Dict[str, Any]
    ) -> str:
        """
        生成题目

        Args:
            context: 上下文信息

        Returns:
            题目内容
        """
        # 构建提示词
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an English interview examiner for graduate school admission."),
            HumanMessage(content=f"""
            Based on the following context, generate an interview question:

            Context:
            - University: {context.get('university', 'General')}
            - Major: {context.get('major', 'General')}
            - Category: {context.get('category', 'General')}
            - Previous questions: {context.get('previous_questions', [])}
            - Question count: {context.get('question_count', 0)}

            Generate a relevant and challenging question.
            Keep it concise and clear.
            """)
        ])

        # 调用LLM
        messages = prompt.format_messages(**context)
        response = self.llm(messages)

        return response.content

    def generate_feedback(
        self,
        question: str,
        answer: str,
        score: Dict[str, Any]
    ) -> str:
        """
        生成反馈

        Args:
            question: 题目
            answer: 回答
            score: 评分结果

        Returns:
            反馈内容
        """
        # 构建提示词
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an English speaking examiner providing feedback."),
            HumanMessage(content=f"""
            Question: {question}
            Answer: {answer}

            Scores:
            - Overall: {score.get('overall_score', 0)}
            - Pronunciation: {score.get('dimensions', {}).get('pronunciation', {}).get('score', 0)}
            - Fluency: {score.get('dimensions', {}).get('fluency', {}).get('score', 0)}
            - Vocabulary: {score.get('dimensions', {}).get('vocabulary', {}).get('score', 0)}
            - Grammar: {score.get('dimensions', {}).get('grammar', {}).get('score', 0)}

            Please provide constructive feedback in 2-3 sentences.
            Focus on the strengths and areas for improvement.
            """)
        ])

        # 调用LLM
        messages = prompt.format_messages(
            question=question,
            answer=answer,
            score=score
        )
        response = self.llm(messages)

        return response.content

    def generate_follow_up(
        self,
        question: str,
        answer: str,
        pressure_level: int = 2,
        tutor_style_id: Optional[str] = None
    ) -> List[str]:
        """
        生成追问

        Args:
            question: 题目
            answer: 回答
            pressure_level: 压力等级
            tutor_style_id: 导师风格ID

        Returns:
            追问列表
        """
        # 构建提示词
        pressure_desc = {
            1: "gentle and encouraging",
            2: "normal and professional",
            3: "challenging and probing"
        }

        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an English interview examiner."),
            HumanMessage(content=f"""
            Question: {question}
            Answer: {answer}
            Pressure level: {pressure_desc.get(pressure_level, 'normal')}

            Generate 1-2 follow-up questions based on the answer.
            The questions should be relevant and challenging.
            If the pressure level is high, ask more probing questions.
            """)
        ])

        # 调用LLM
        messages = prompt.format_messages(
            question=question,
            answer=answer,
            pressure_level=pressure_level
        )
        response = self.llm(messages)

        # 解析追问
        follow_up_text = response.content
        follow_up_questions = self._parse_follow_up(follow_up_text)

        return follow_up_questions

    def enhance_expression(
        self,
        original_text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        增强表达

        Args:
            original_text: 原始文本
            context: 上下文信息

        Returns:
            增强后的表达
        """
        # 构建提示词
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an English language expert."),
            HumanMessage(content=f"""
            Original text: {original_text}

            Please enhance this text to make it more academic and professional.
            Provide:
            1. Enhanced version
            2. Key improvements made
            3. Advanced vocabulary used

            Return in JSON format:
            {{
                "enhanced": "enhanced text",
                "improvements": ["improvement 1", "improvement 2"],
                "advanced_vocabulary": ["word1", "word2"]
            }}
            """)
        ])

        # 调用LLM
        messages = prompt.format_messages(original_text=original_text)
        response = self.llm(messages)

        # 解析结果
        import json
        try:
            result = json.loads(response.content)
        except:
            result = {
                "enhanced": original_text,
                "improvements": [],
                "advanced_vocabulary": []
            }

        return result

    def _parse_follow_up(self, text: str) -> List[str]:
        """
        解析追问文本

        Args:
            text: 追问文本

        Returns:
            追问列表
        """
        # 简单实现：按行分割
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return lines

    def get_model_info(self) -> Dict[str, Any]:
        """
        获取模型信息

        Returns:
            模型信息
        """
        return {
            "model_name": self.model_name,
            "temperature": 0.7,
            "max_tokens": 1000
        }


class LLMConfig:
    """LLM配置"""

    # 模型配置
    MODELS = {
        "qwen2.5-7b": {
            "name": "Qwen2.5-7B",
            "provider": "Qwen",
            "description": "7B参数模型，适合通用场景"
        },
        "qwen2.5-72b": {
            "name": "Qwen2.5-72B",
            "provider": "Qwen",
            "description": "72B参数模型，适合复杂任务"
        },
        "deepseek-r1": {
            "name": "DeepSeek-R1",
            "provider": "DeepSeek",
            "description": "高性能推理模型"
        }
    }

    # 推荐模型
    RECOMMENDED_MODELS = {
        "general": "qwen2.5-7b",
        "complex": "qwen2.5-72b",
        "reasoning": "deepseek-r1"
    }

    # 温度配置
    TEMPERATURE = {
        "precise": 0.3,
        "balanced": 0.7,
        "creative": 1.0
    }

    @classmethod
    def get_model_info(cls, model_name: str) -> Dict[str, str]:
        """
        获取模型信息
        """
        return cls.MODELS.get(model_name, {})

    @classmethod
    def get_recommended_model(cls, use_case: str) -> str:
        """
        获取推荐模型
        """
        return cls.RECOMMENDED_MODELS.get(use_case, "qwen2.5-7b")