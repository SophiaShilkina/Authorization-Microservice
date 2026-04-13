from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from ...persistence.postgres.ports import ITransactionManager, IInboxRepository

from ...persistence.postgres.sqlalchemy.transaction import SqlAlchemyTransactionManager
from ...persistence.postgres.executors import HttpExecutor, KafkaExecutor


class ExecutorProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def transaction_manager(self, session: AsyncSession) -> ITransactionManager:
        return SqlAlchemyTransactionManager(session)

    @provide(scope=Scope.REQUEST)
    def http_executor(self, tx_manager: SqlAlchemyTransactionManager) -> HttpExecutor:
        return HttpExecutor(tx_manager)

    @provide(scope=Scope.REQUEST)
    def kafka_executor(self,
                       tx_manager: SqlAlchemyTransactionManager,
                       inbox_repository: IInboxRepository) -> KafkaExecutor:
        return KafkaExecutor(tx_manager, inbox_repository)
