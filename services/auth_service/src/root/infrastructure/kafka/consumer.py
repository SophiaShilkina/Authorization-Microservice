import asyncio
import json
import logging
from typing import Callable, Awaitable, Optional

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

from ..exceptions import KafkaConsumerError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KafkaConsumerClient:
    """
    Использование:
        consumer = KafkaConsumerClient('orders', handler_func)
        await consumer.start()
    """

    def __init__(
            self,
            bootstrap_servers: list[str],
            offset_reset: str,
            enable_auto_commit: bool,
            topic: str,
            handler: Callable[[dict], Awaitable[None]],
            group_id: Optional[str] = None,
    ):
        self._bootstrap_servers = bootstrap_servers
        self._offset_reset = offset_reset
        self._enable_auto_commit = enable_auto_commit

        self.topic = topic
        self.handler = handler
        self.group_id = group_id
        self.consumer: Optional[AIOKafkaConsumer] = None
        self._running = False

    async def start(self):
        """Создаёт consumer и начинает обработку"""
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self._bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset=self._offset_reset,
            enable_auto_commit=self._enable_auto_commit,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        )

        await self.consumer.start()
        logger.info(f'Consumer started for topic: {self.topic}')

        self._running = True
        asyncio.create_task(self._consume_loop())

    async def stop(self):
        """Останавливает consumer"""
        self._running = False
        if self.consumer:
            await self.consumer.stop()
            logger.info(f'Consumer stopped for topic: {self.topic}')

    async def _consume_loop(self):
        """Основной цикл чтения событий"""
        try:
            async for message in self.consumer:
                try:
                    # Обрабатываем событие
                    await self.handler(message.value)

                    # Commit offset после успешной обработки
                    await self.consumer.commit()

                    logger.debug(
                        f'Processed message from {self.topic}: '
                        f'partition={message.partition}, offset={message.offset}'
                    )

                except Exception as error:
                    logger.error(f'Error processing message: {error}', exc_info=True)
                    # Не делаем commit → сообщение будет перечитано

        except KafkaError as error:
            logger.error(f'Consumer error: {error}')
            raise KafkaConsumerError(f'Consumer error: {error}')
        except Exception as error:
            logger.error(f'Unexpected error: {error}', exc_info=True)
            raise KafkaConsumerError(f'Consumer error: {error}')
