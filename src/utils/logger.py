# 日志器伪代码
# 文件路径: utils/logger.py

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional


class JSONFormatter(logging.Formatter):
    """JSON日志格式化器"""

    def format(self, record: logging.LogRecord) -> str:
        """
        格式化日志记录

        Args:
            record: 日志记录

        Returns:
            JSON格式的日志字符串
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # 添加额外字段
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id

        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id

        if hasattr(record, 'session_id'):
            log_data['session_id'] = record.session_id

        if hasattr(record, 'trace_id'):
            log_data['trace_id'] = record.trace_id

        # 添加异常信息
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


class Logger:
    """日志器"""

    _instances = {}

    def __new__(cls, name: str = "empenglish"):
        """
        创建或获取日志器实例

        Args:
            name: 日志器名称

        Returns:
            日志器实例
        """
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
            cls._instances[name]._initialized = False
        return cls._instances[name]

    def __init__(self, name: str = "empenglish"):
        """
        初始化日志器

        Args:
            name: 日志器名称
        """
        if self._initialized:
            return

        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # 清除现有处理器
        self.logger.handlers.clear()

        # 添加处理器
        self._add_console_handler()
        self._add_file_handler()

        self._initialized = True

    def _add_console_handler(self):
        """
        添加控制台处理器
        """
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(console_handler)

    def _add_file_handler(self):
        """
        添加文件处理器
        """
        # 伪代码：实际实现需要创建日志文件
        # from pathlib import Path
        #
        # log_dir = Path("logs")
        # log_dir.mkdir(exist_ok=True)
        #
        # file_handler = logging.FileHandler(
        #     log_dir / f"{self.name}.log",
        #     encoding='utf-8'
        # )
        # file_handler.setLevel(logging.INFO)
        # file_handler.setFormatter(JSONFormatter())
        # self.logger.addHandler(file_handler)
        pass

    def info(
        self,
        message: str,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        session_id: Optional[str] = None,
        **kwargs
    ):
        """
        记录信息日志

        Args:
            message: 日志消息
            user_id: 用户ID
            request_id: 请求ID
            session_id: 会话ID
            **kwargs: 额外字段
        """
        extra = {
            "user_id": user_id,
            "request_id": request_id,
            "session_id": session_id
        }
        extra.update(kwargs)

        self.logger.info(message, extra=extra)

    def warning(
        self,
        message: str,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        session_id: Optional[str] = None,
        **kwargs
    ):
        """
        记录警告日志

        Args:
            message: 日志消息
            user_id: 用户ID
            request_id: 请求ID
            session_id: 会话ID
            **kwargs: 额外字段
        """
        extra = {
            "user_id": user_id,
            "request_id": request_id,
            "session_id": session_id
        }
        extra.update(kwargs)

        self.logger.warning(message, extra=extra)

    def error(
        self,
        message: str,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        session_id: Optional[str] = None,
        exc_info: Optional[Any] = None,
        **kwargs
    ):
        """
        记录错误日志

        Args:
            message: 日志消息
            user_id: 用户ID
            request_id: 请求ID
            session_id: 会话ID
            exc_info: 异常信息
            **kwargs: 额外字段
        """
        extra = {
            "user_id": user_id,
            "request_id": request_id,
            "session_id": session_id
        }
        extra.update(kwargs)

        self.logger.error(message, exc_info=exc_info, extra=extra)

    def debug(
        self,
        message: str,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        session_id: Optional[str] = None,
        **kwargs
    ):
        """
        记录调试日志

        Args:
            message: 日志消息
            user_id: 用户ID
            request_id: 请求ID
            session_id: 会话ID
            **kwargs: 额外字段
        """
        extra = {
            "user_id": user_id,
            "request_id": request_id,
            "session_id": session_id
        }
        extra.update(kwargs)

        self.logger.debug(message, extra=extra)


class RequestContext:
    """请求上下文"""

    _context = {}

    @classmethod
    def set(cls, key: str, value: Any):
        """
        设置上下文值

        Args:
            key: 键
            value: 值
        """
        cls._context[key] = value

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        获取上下文值

        Args:
            key: 键
            default: 默认值

        Returns:
            值
        """
        return cls._context.get(key, default)

    @classmethod
    def clear(cls):
        """
        清除上下文
        """
        cls._context.clear()

    @classmethod
    def get_context(cls) -> Dict[str, Any]:
        """
        获取所有上下文

        Returns:
            上下文字典
        """
        return cls._context.copy()


class LogMiddleware:
    """日志中间件"""

    def __init__(self, logger: Logger):
        """
        初始化日志中间件

        Args:
            logger: 日志器
        """
        self.logger = logger

    async def log_request(self, request: Any):
        """
        记录请求

        Args:
            request: 请求对象
        """
        # 伪代码：实际实现需要从请求中提取信息
        # request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        # user_id = request.state.get("user_id")
        #
        # RequestContext.set("request_id", request_id)
        # RequestContext.set("user_id", user_id)
        #
        # self.logger.info(
        #     f"Request started: {request.method} {request.url.path}",
        #     request_id=request_id,
        #     user_id=user_id,
        #     method=request.method,
        #     path=request.url.path,
        #     query_params=dict(request.query_params)
        # )
        pass

    async def log_response(self, request: Any, response: Any, duration: float):
        """
        记录响应

        Args:
            request: 请求对象
            response: 响应对象
            duration: 处理时长
        """
        # 伪代码：实际实现需要从响应中提取信息
        # request_id = RequestContext.get("request_id")
        # user_id = RequestContext.get("user_id")
        # status_code = response.status_code
        #
        # self.logger.info(
        #     f"Request completed: {request.method} {request.url.path}",
        #     request_id=request_id,
        #     user_id=user_id,
        #     status_code=status_code,
        #     duration=duration
        # )
        #
        # RequestContext.clear()
        pass


class LoggerConfig:
    """日志配置"""

    # 日志级别
    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    # 日志格式
    LOG_FORMATS = {
        "json": JSONFormatter,
        "text": logging.Formatter
    }

    # 日志文件配置
    LOG_FILES = {
        "app": "logs/app.log",
        "error": "logs/error.log",
        "access": "logs/access.log"
    }

    # 日志轮转配置
    LOG_ROTATION = {
        "max_size": "100MB",
        "backup_count": 10
    }

    @classmethod
    def get_log_level(cls, level: str) -> int:
        """
        获取日志级别

        Args:
            level: 级别名称

        Returns:
            日志级别常量
        """
        return cls.LOG_LEVELS.get(level.upper(), logging.INFO)

    @classmethod
    def should_log_to_file(cls, log_type: str) -> bool:
        """
        检查是否应该记录到文件

        Args:
            log_type: 日志类型

        Returns:
            是否记录到文件
        """
        return log_type in cls.LOG_FILES